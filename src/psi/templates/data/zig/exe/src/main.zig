# ${project_name} - Executable

const std = @import("std");

pub fn main() !void {
    std.debug.print("Hello from ${project_name}!\n", .{});
}