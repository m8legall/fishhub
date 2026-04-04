import fastify from "./app.js";

/**
 * Run the server!
 */
const start = async () => {
  try {
    await fastify.listen({ port: process.env.PORT || 3000 })
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}

console.log('Bienvenue sur le backend de notre application sociale !');
start()