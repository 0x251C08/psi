import Fastify from "fastify";
import cors from "@fastify/cors";

const fastify = Fastify({ logger: true });

await fastify.register(cors, { origin: true });

fastify.get("/", async () => {
  return { message: "Welcome to ${project_name}" };
});

fastify.get("/health", async () => {
  return { status: "ok" };
});

fastify.post("/items", async (request) => {
  return request.body;
});

fastify.get("/items/:id", async (request) => {
  return { item_id: parseInt(request.params.id), name: `Item ${request.params.id}` });
});

const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: "0.0.0.0" });
    console.log("Server running on http://localhost:3000");
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();