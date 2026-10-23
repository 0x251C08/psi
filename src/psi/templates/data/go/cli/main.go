package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "${project_name}",
	Short: "A CLI application",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Welcome to ${project_name}!")
	},
}

var helloCmd = &cobra.Command{
	Use:   "hello [name]",
	Short: "Say hello",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := "World"
		if len(args) > 0 {
			name = args[0]
		}
		fmt.Printf("Hello, %s!\n", name)
	},
}

var goodbyeCmd = &cobra.Command{
	Use:   "goodbye [name]",
	Short: "Say goodbye",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := "World"
		if len(args) > 0 {
			name = args[0]
		}
		fmt.Printf("Goodbye, %s!\n", name)
	},
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Show version",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("${project_name} v0.1.0")
	},
}

func main() {
	rootCmd.AddCommand(helloCmd, goodbyeCmd, versionCmd)
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}