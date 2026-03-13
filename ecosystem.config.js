const path = require("path");

const rootDir = __dirname;
const logsDir = path.join(rootDir, "logs");

module.exports = {
  apps: [
    {
      name: "backend-service",
      cwd: path.join(rootDir, "MilkMan", "backend"),
      script: path.join(rootDir, "scripts", "start-backend.sh"),
      interpreter: "/bin/bash",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      time: true,
      merge_logs: true,
      log_file: path.join(logsDir, "backend.log"),
      env: {
        NODE_ENV: process.env.NODE_ENV || "production",
        HOST: process.env.HOST || "0.0.0.0",
        PORT: process.env.PORT || "5000",
        DATABASE_URL: process.env.DATABASE_URL || "sqlite:///milkman.db",
        JWT_SECRET: process.env.JWT_SECRET || "change-me-in-production",
        JWT_SECRET_KEY: process.env.JWT_SECRET_KEY || process.env.JWT_SECRET || "change-me-in-production",
        FLASK_DEBUG: "false",
        PYTHONUNBUFFERED: "1",
      },
    },
    {
      name: "admin-dashboard",
      cwd: path.join(rootDir, "MilkMan", "frontend"),
      script: path.join(rootDir, "scripts", "static-server.js"),
      interpreter: "node",
      args: "--root . --host 0.0.0.0 --port 3000 --fallback index.html",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      time: true,
      merge_logs: true,
      log_file: path.join(logsDir, "admin.log"),
      env: {
        NODE_ENV: process.env.NODE_ENV || "production",
        HOST: "0.0.0.0",
        PORT: "3000",
      },
    },
    {
      name: "customer-website",
      cwd: path.join(rootDir, "MilkMan", "customer-site"),
      script: path.join(rootDir, "scripts", "static-server.js"),
      interpreter: "node",
      args: "--root . --host 0.0.0.0 --port 3001 --fallback index.html",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      time: true,
      merge_logs: true,
      log_file: path.join(logsDir, "customer.log"),
      env: {
        NODE_ENV: process.env.NODE_ENV || "production",
        HOST: "0.0.0.0",
        PORT: "3001",
      },
    },
  ],
};