#!/usr/bin/env python3
"""
QtLiveDevTools MCP Server

Provides Qt UI development tools for Claude CLI.
Run with: python qtlivedevtools_mcp.py
"""

import asyncio
import sys
import logging
import traceback
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pathlib import Path
import json

# Configure logging to stderr (MCP uses stdout for protocol)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("qtlivedevtools")

# Import our existing functions
logger.info("Importing mcp_server functions...")
try:
    from mcp_server import (
        create_ui_file,
        add_widget_to_ui,
        add_layout_to_ui,
        modify_widget_property,
        get_ui_structure,
        preview_ui,
        analyze_ui,
        send_command_to_editor
    )
    logger.info("✓ Successfully imported all mcp_server functions")
except Exception as e:
    logger.error(f"✗ Failed to import mcp_server functions: {e}")
    logger.error(traceback.format_exc())
    raise

# Create MCP server
logger.info("Creating MCP server instance...")
app = Server("qtlivedevtools")
logger.info("✓ MCP server instance created")

# Default editor port
DEFAULT_PORT = 7010


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Qt UI development tools."""
    logger.debug("list_tools() called")
    return [
        Tool(
            name="create_ui_file",
            description="Create a new Qt .ui file from template (dialog, mainwindow, or widget)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "UI file name (without .ui extension)"
                    },
                    "template": {
                        "type": "string",
                        "enum": ["dialog", "mainwindow", "widget"],
                        "description": "Template type",
                        "default": "dialog"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Initial width in pixels",
                        "default": 400
                    },
                    "height": {
                        "type": "integer",
                        "description": "Initial height in pixels",
                        "default": 300
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="add_widget",
            description="Add a widget to existing .ui file (QPushButton, QLabel, QLineEdit, QListWidget, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "ui_file": {
                        "type": "string",
                        "description": "Path to .ui file"
                    },
                    "widget_type": {
                        "type": "string",
                        "description": "Widget class name (e.g., QPushButton, QLabel, QLineEdit)"
                    },
                    "object_name": {
                        "type": "string",
                        "description": "Unique object name for the widget"
                    },
                    "properties": {
                        "type": "object",
                        "description": "Widget properties (text, geometry, etc.)",
                        "default": {}
                    }
                },
                "required": ["ui_file", "widget_type", "object_name"]
            }
        ),
        Tool(
            name="add_layout",
            description="Add a layout to .ui file (QVBoxLayout, QHBoxLayout, QGridLayout)",
            inputSchema={
                "type": "object",
                "properties": {
                    "ui_file": {
                        "type": "string",
                        "description": "Path to .ui file"
                    },
                    "layout_type": {
                        "type": "string",
                        "enum": ["QVBoxLayout", "QHBoxLayout", "QGridLayout"],
                        "description": "Layout class name"
                    },
                    "object_name": {
                        "type": "string",
                        "description": "Unique object name for the layout"
                    }
                },
                "required": ["ui_file", "layout_type", "object_name"]
            }
        ),
        Tool(
            name="modify_property",
            description="Modify a widget property in .ui file",
            inputSchema={
                "type": "object",
                "properties": {
                    "ui_file": {
                        "type": "string",
                        "description": "Path to .ui file"
                    },
                    "widget_name": {
                        "type": "string",
                        "description": "Widget object name"
                    },
                    "property_name": {
                        "type": "string",
                        "description": "Property to modify (e.g., text, geometry)"
                    },
                    "value": {
                        "description": "New value (string, number, or object for complex properties)"
                    }
                },
                "required": ["ui_file", "widget_name", "property_name", "value"]
            }
        ),
        Tool(
            name="get_ui_structure",
            description="Get complete widget hierarchy from .ui file",
            inputSchema={
                "type": "object",
                "properties": {
                    "ui_file": {
                        "type": "string",
                        "description": "Path to .ui file"
                    }
                },
                "required": ["ui_file"]
            }
        ),
        Tool(
            name="preview_ui",
            description="Preview UI in Live Editor and take screenshot (requires Live Editor running)",
            inputSchema={
                "type": "object",
                "properties": {
                    "ui_file": {
                        "type": "string",
                        "description": "Path to .ui file"
                    },
                    "port": {
                        "type": "integer",
                        "description": "Editor port",
                        "default": DEFAULT_PORT
                    }
                },
                "required": ["ui_file"]
            }
        ),
        Tool(
            name="analyze_ui",
            description="Complete multi-layer UI analysis (XML structure + screenshot if Live Editor running)",
            inputSchema={
                "type": "object",
                "properties": {
                    "ui_file": {
                        "type": "string",
                        "description": "Path to .ui file"
                    },
                    "port": {
                        "type": "integer",
                        "description": "Editor port",
                        "default": DEFAULT_PORT
                    }
                },
                "required": ["ui_file"]
            }
        ),
        Tool(
            name="send_editor_command",
            description="Send custom command to Live UI Editor (reload, screenshot, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command action (ping, reload_ui, take_screenshot, get_widget_tree)"
                    },
                    "port": {
                        "type": "integer",
                        "description": "Editor port",
                        "default": DEFAULT_PORT
                    }
                },
                "required": ["command"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool."""
    logger.info(f"Tool called: {name}")
    logger.debug(f"Arguments: {json.dumps(arguments, indent=2)}")

    try:
        result = None

        if name == "create_ui_file":
            logger.debug("Executing create_ui_file...")
            result = create_ui_file(
                arguments["name"],
                arguments.get("template", "dialog"),
                arguments.get("width", 400),
                arguments.get("height", 300)
            )

        elif name == "add_widget":
            result = add_widget_to_ui(
                arguments["ui_file"],
                arguments["widget_type"],
                arguments["object_name"],
                None,  # parent_name
                arguments.get("properties", {})
            )

        elif name == "add_layout":
            result = add_layout_to_ui(
                arguments["ui_file"],
                arguments["layout_type"],
                arguments["object_name"],
                None  # parent_name
            )

        elif name == "modify_property":
            result = modify_widget_property(
                arguments["ui_file"],
                arguments["widget_name"],
                arguments["property_name"],
                arguments["value"]
            )

        elif name == "get_ui_structure":
            result = get_ui_structure(arguments["ui_file"])

        elif name == "preview_ui":
            result = preview_ui(
                arguments["ui_file"],
                arguments.get("port", DEFAULT_PORT)
            )

        elif name == "analyze_ui":
            result = analyze_ui(
                arguments["ui_file"],
                arguments.get("port", DEFAULT_PORT)
            )

        elif name == "send_editor_command":
            result = send_command_to_editor(
                arguments["command"],
                arguments.get("port", DEFAULT_PORT)
            )

        else:
            logger.warning(f"Unknown tool requested: {name}")
            result = {"status": "error", "message": f"Unknown tool: {name}"}

        # Format response
        logger.debug(f"Tool {name} result: {result.get('status', 'unknown')}")
        response_text = json.dumps(result, indent=2, ensure_ascii=False)

        return [TextContent(type="text", text=response_text)]

    except Exception as e:
        logger.error(f"Exception in tool {name}: {e}")
        logger.error(traceback.format_exc())
        error_response = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "tool": name,
            "arguments": arguments
        }
        return [TextContent(type="text", text=json.dumps(error_response, indent=2))]


async def main():
    """Run the MCP server."""
    logger.info("="*60)
    logger.info("QtLiveDevTools MCP Server Starting")
    logger.info(f"Working directory: {Path.cwd()}")
    logger.info(f"Default editor port: {DEFAULT_PORT}")
    logger.info("="*60)

    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("stdio_server initialized, starting main loop...")
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Fatal error in main(): {e}")
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    logger.info("Script started")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
