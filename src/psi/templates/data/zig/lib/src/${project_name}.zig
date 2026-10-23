# ${project_name} - Library

const std = @import("std");

pub fn hello(name: []const u8) []const u8 {
    return std.fmt.allocPrint(std.heap.page_allocator, "Hello, {s}!", .{name}) catch "Hello!";
}

pub fn add(a: i32, b: i32) i32 {
    return a + b;
}