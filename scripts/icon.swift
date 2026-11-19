import AppKit
import Foundation

// A simple code-drawn Ugram placeholder icon; no Telegram logo assets are copied.
let folder = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
let size = 1024
let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
    bitsPerSample: 8, samplesPerPixel: 3, hasAlpha: false, isPlanar: false,
    colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
NSColor(calibratedRed: 0.04, green: 0.54, blue: 0.44, alpha: 1).setFill()
NSBezierPath(rect: NSRect(x: 0, y: 0, width: CGFloat(size), height: CGFloat(size))).fill()
let u = NSBezierPath()
u.lineWidth = 116
u.lineCapStyle = .round
u.move(to: NSPoint(x: 300, y: 735))
u.line(to: NSPoint(x: 300, y: 440))
u.curve(to: NSPoint(x: 724, y: 440),
        controlPoint1: NSPoint(x: 300, y: 175), controlPoint2: NSPoint(x: 724, y: 175))
u.line(to: NSPoint(x: 724, y: 735))
NSColor.white.setStroke()
u.stroke()
NSGraphicsContext.restoreGraphicsState()
try bitmap.representation(using: .png, properties: [:])!.write(to: folder.appendingPathComponent("Ugram.png"))
let contents = """
{"images":[{"filename":"Ugram.png","idiom":"universal","platform":"ios","size":"1024x1024"}],"info":{"author":"Ugram","version":1}}
"""
try contents.write(to: folder.appendingPathComponent("Contents.json"), atomically: true, encoding: .utf8)
