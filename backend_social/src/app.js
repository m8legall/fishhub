// Importing Fastify framework to create the server
import Fastify from 'fastify';

const fastify = Fastify({ 
    logger: true
});

// Registering a simple route to test the server
fastify.get('/', async (request, reply) => {
  return { hello: 'world' }
})




export default fastify