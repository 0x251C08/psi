use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "${project_name}", version, about = "A CLI application")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Say hello
    Hello {
        #[arg(default_value = "World")]
        name: String,
    },
    /// Say goodbye
    Goodbye {
        #[arg(default_value = "World")]
        name: String,
    },
    /// Show version
    Version,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Hello { name } => println!("Hello, {}!", name),
        Commands::Goodbye { name } => println!("Goodbye, {}!", name),
        Commands::Version => println!("${project_name} v0.1.0"),
    }
}