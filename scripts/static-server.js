#!/usr/bin/env node

const fs = require("fs");
const http = require("http");
const path = require("path");

const args = process.argv.slice(2);
const options = {
  root: process.cwd(),
  host: process.env.HOST || "0.0.0.0",
  port: Number(process.env.PORT || 3000),
  fallback: "",
};

for (let i = 0; i < args.length; i += 1) {
  const arg = args[i];
  if (arg === "--root") options.root = path.resolve(args[i + 1]);
  if (arg === "--host") options.host = args[i + 1];
  if (arg === "--port") options.port = Number(args[i + 1]);
  if (arg === "--fallback") options.fallback = args[i + 1];
}

const mimeTypes = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp",
  ".avif": "image/avif",
};

function sendFile(filePath, res) {
  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("Not Found");
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": contentType, "Cache-Control": "no-cache" });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  let requestPath = decodeURIComponent(url.pathname);

  if (requestPath === "/") {
    requestPath = "/index.html";
  }

  const safePath = path.normalize(requestPath).replace(/^([.][.][/\\])+/, "");
  const resolvedPath = path.resolve(options.root, `.${safePath}`);

  if (!resolvedPath.startsWith(options.root)) {
    res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Forbidden");
    return;
  }

  fs.stat(resolvedPath, (statError, stats) => {
    if (!statError && stats.isFile()) {
      sendFile(resolvedPath, res);
      return;
    }

    if (!statError && stats.isDirectory()) {
      const indexFile = path.join(resolvedPath, "index.html");
      if (fs.existsSync(indexFile)) {
        sendFile(indexFile, res);
        return;
      }
    }

    if (options.fallback) {
      const fallbackPath = path.resolve(options.root, options.fallback);
      if (fallbackPath.startsWith(options.root) && fs.existsSync(fallbackPath)) {
        sendFile(fallbackPath, res);
        return;
      }
    }

    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not Found");
  });
});

server.listen(options.port, options.host, () => {
  console.log(`Static server running from ${options.root} at http://${options.host}:${options.port}`);
});