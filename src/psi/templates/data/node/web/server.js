import express from "express";
import cors from "cors";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({ message: "Welcome to ${project_name}" });
});

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.post("/items", (req, res) => {
  res.status(201).json(req.body);
});

app.get("/items/:id", (req, res) => {
  res.json({ item_id: parseInt(req.params.id), name: `Item ${req.params.id}` });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});