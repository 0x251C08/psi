/**
 * ${project_name} - A Node.js package
 */

export function hello(name = "World") {
  return `Hello, ${name}!`;
}

export function add(a, b) {
  return a + b;
}

export default { hello, add };