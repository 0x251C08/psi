const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const lib = b.addStaticLibrary(.{
        .name = "${project_name}",
        .root_source_file = b.path("src/${project_name}.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(lib);

    const test_step = b.step("test", "Run tests");
    const test = b.addTest(.{
        .root_source_file = b.path("src/${project_name}.zig"),
        .target = target,
        .optimize = optimize,
    });
    test_step.dependOn(&test.step);
}