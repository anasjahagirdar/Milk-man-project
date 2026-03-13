const express = require("express");
const path = require("path");

const app = express();
const frontendRoot = __dirname;
const customerRoot = path.resolve(__dirname, "..", "customer-site");
const port = Number(process.env.PORT || 3000);
const host = process.env.HOST || "0.0.0.0";

app.use(express.static(frontendRoot));
app.use("/customer", express.static(customerRoot));

app.get("/customer", (_req, res) => {
  res.sendFile(path.join(customerRoot, "index.html"));
});

app.get("/", (_req, res) => {
  res.sendFile(path.join(frontendRoot, "index.html"));
});

app.use((req, res, next) => {
  if (req.path.startsWith("/customer/")) {
    return res.sendFile(path.join(customerRoot, req.path.replace(/^\/customer\//, "")));
  }
  if (path.extname(req.path)) {
    return next();
  }
  return res.sendFile(path.join(frontendRoot, "index.html"));
});

app.listen(port, host, () => {
  console.log(`MilkMan frontend running at http://${host}:${port}`);
  console.log(`MilkMan customer site running at http://${host}:${port}/customer/`);
});
