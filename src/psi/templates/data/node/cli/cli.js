#!/usr/bin/env node
import { Command } from "commander";

const program = new Command();

program
  .name("${project_name}")
  .description("A CLI application")
  .version("0.1.0");

program
  .command("hello [name]")
  .description("Say hello")
  .action((name = "World") => {
    console.log(`Hello, ${name}!`);
  });

program
  .command("goodbye [name]")
  .description("Say goodbye")
  .action((name = "World") => {
    console.log(`Goodbye, ${name}!`);
  });

program
  .command("version")
  .description("Show version")
  .action(() => {
    console.log("${project_name} v0.1.0");
  });

program.parse(process.argv);