"""Serving command logic."""

import http.server
import socketserver
import webbrowser
import click


def start_server(port: int, open_browser: bool):
    """Serves the HTML report locally."""
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}/PROJECT_SUMMARY.html"
            click.secho(f"🌐 Serving report at: {url}", fg="cyan")
            if open_browser:
                webbrowser.open(url)
            httpd.serve_forever()
    except KeyboardInterrupt:
        click.echo("\n🛑 Server stopped.")
    except Exception as e:
        click.secho(f"❌ Server error: {e}", fg="red")
