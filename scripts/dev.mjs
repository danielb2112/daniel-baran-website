#!/usr/bin/env node

import { spawn } from "node:child_process";
import fs from "node:fs";
import fsp from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIST = path.join(ROOT, "dist");
const PORT = Number(process.env.PORT || 4173);
const RELOAD_SNIPPET = `<script>
new EventSource("/__reload").addEventListener("message", function () { window.location.reload(); });
</script>`;

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

const clients = new Set();
let buildRunning = false;
let pendingBuild = false;
let debounceTimer = null;

function runBuild() {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(ROOT, "scripts", "build-static.mjs")], {
      cwd: ROOT,
      stdio: "inherit",
    });
    child.on("exit", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`Build failed with exit code ${code}`));
    });
  });
}

async function rebuild() {
  if (buildRunning) {
    pendingBuild = true;
    return;
  }

  buildRunning = true;
  try {
    await runBuild();
    for (const response of clients) response.write("event: message\ndata: reload\n\n");
  } catch (error) {
    console.error(error.message);
  } finally {
    buildRunning = false;
    if (pendingBuild) {
      pendingBuild = false;
      rebuild();
    }
  }
}

function scheduleRebuild() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(rebuild, 120);
}

function watchPath(relativePath) {
  const absolute = path.join(ROOT, relativePath);
  if (!fs.existsSync(absolute)) return;

  fs.watch(absolute, { recursive: true }, (_event, changedPath = "") => {
    const changed = String(changedPath);
    if (
      changed.startsWith("dist") ||
      changed.startsWith(".git") ||
      changed.includes("__pycache__") ||
      changed.includes("assets/bundle")
    ) {
      return;
    }
    scheduleRebuild();
  });
}

async function resolveRequest(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?", 1)[0]);
  const normalized = path.normalize(decoded).replace(/^(\.\.[/\\])+/, "");
  let file = path.join(DIST, normalized);

  if (!file.startsWith(DIST)) return null;
  const stat = await fsp.stat(file).catch(() => null);
  if (stat?.isDirectory()) file = path.join(file, "index.html");
  return file;
}

async function sendFile(response, file) {
  const stat = await fsp.stat(file).catch(() => null);
  if (!stat || !stat.isFile()) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
    return;
  }

  let body = await fsp.readFile(file);
  const ext = path.extname(file).toLowerCase();
  const type = TYPES[ext] || "application/octet-stream";
  if (ext === ".html") {
    body = Buffer.from(body.toString("utf8").replace("</body>", `${RELOAD_SNIPPET}</body>`));
  }

  response.writeHead(200, {
    "content-type": type,
    "cache-control": "no-store",
  });
  response.end(body);
}

async function main() {
  await rebuild();

  ["index.html", "ueber-mich", "projekte", "en", "pl", "impressum", "datenschutz", "assets/site.js", "_headers"].forEach(watchPath);

  const server = http.createServer(async (request, response) => {
    if (request.url === "/__reload") {
      response.writeHead(200, {
        "content-type": "text/event-stream",
        "cache-control": "no-store",
        connection: "keep-alive",
      });
      response.write("\n");
      clients.add(response);
      request.on("close", () => clients.delete(response));
      return;
    }

    const file = await resolveRequest(request.url || "/");
    if (!file) {
      response.writeHead(400, { "content-type": "text/plain; charset=utf-8" });
      response.end("Bad request");
      return;
    }
    sendFile(response, file);
  });

  server.listen(PORT, "127.0.0.1", () => {
    console.log(`dev server: http://127.0.0.1:${PORT}/`);
  });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
