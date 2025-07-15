import reactpy
from reactpy import html, component, use_state
import requests

@component
def NameLookupApp():
    id_value, set_id_value = use_state("")
    pending_value, set_pending_value = use_state("")
    error, set_error = use_state("")
    name, set_name = use_state("")

    def handle_lookup(event):
        print(f"Current pending_value: {pending_value}")
        set_error("")
        set_name("")
        # Validate input
        if not pending_value.strip() or not pending_value.isdigit():
            set_error("Please enter a valid numeric ID")
            return
        set_id_value(pending_value)  # Only update id_value on click
        try:
            resp = requests.post(
                "http://host.docker.internal:8080/getName",
                json={"id": int(pending_value)},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            print(f"Response: {resp.status_code} {resp.text}")
            if resp.status_code == 200:
                data = resp.json()
                name_val = data.get("name")
                if name_val is None or name_val == "null":
                    set_name("No name for this id")
                else:
                    set_name(name_val)
            else:
                set_error(f"Error: {resp.status_code}")
        except Exception as e:
            set_error(str(e))
        finally:
            print(f"pending_value after lookup: {pending_value}")

    def handle_input_change(event):
        new_value = event["target"]["value"]
        print(f"Input changed to: {new_value}")
        set_pending_value(new_value)

    return html.div(
        {
            "style": {
                "fontFamily": "'Segoe UI', 'Roboto', 'Arial', sans-serif",
                "background": "linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%)",
                "minHeight": "100vh",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            }
        },
        html.div(
            {
                "style": {
                    "background": "#fff",
                    "padding": "2.5rem 2rem 2rem 2rem",
                    "borderRadius": "1.2rem",
                    "boxShadow": "0 8px 32px 0 rgba(31, 38, 135, 0.15)",
                    "width": "100%",
                    "maxWidth": "420px",
                }
            },
            html.h2(
                {"style": {"textAlign": "center", "color": "#2d3748", "marginBottom": "1.5rem"}},
                "🔎 Name Lookup",
            ),
            html.div(
                {
                    "style": {"display": "flex", "flexDirection": "column", "gap": "1.2rem"},
                },
                html.label(
                    {"for": "id", "style": {"fontWeight": "bold", "color": "#4a5568"}},
                    "Enter ID:",
                ),
                html.input(
                    {
                        "id": "id",
                        "type": "number",
                        "value": pending_value,
                        "on_change": handle_input_change,
                        "style": {
                            "padding": "0.7em 1em",
                            "border": "1px solid #cbd5e1",
                            "borderRadius": "0.5em",
                            "fontSize": "1.1em",
                            "outline": "none",
                            "transition": "border 0.2s",
                            "marginBottom": "0.5em",
                        },
                    }
                ),
                html.button(
                    {
                        "type": "button",
                        "on_click": handle_lookup,
                        "style": {
                            "background": "linear-gradient(90deg, #667eea 0%, #5a67d8 100%)",
                            "color": "#fff",
                            "padding": "0.7em 1.2em",
                            "border": "none",
                            "borderRadius": "0.5em",
                            "fontWeight": "bold",
                            "fontSize": "1.1em",
                            "cursor": "pointer",
                            "boxShadow": "0 2px 8px rgba(90, 103, 216, 0.08)",
                            "transition": "background 0.2s",
                        },
                    },
                    "Lookup",
                ),
            ),
            html.div(
                {
                    "style": {
                        "marginTop": "1.2em",
                        "minHeight": "2em",
                        "textAlign": "center",
                    }
                },
                (
                    html.p(
                        {
                            "style": {
                                "color": "#22543d" if name and name != "No name for this id" else "#e53e3e",
                                "background": "#e6fffa" if name and name != "No name for this id" else "#fff5f5",
                                "border": "1px solid #38b2ac" if name and name != "No name for this id" else "1px solid #feb2b2",
                                "borderRadius": "0.5em",
                                "padding": "0.8em 1em",
                                "fontWeight": "bold",
                                "fontSize": "1.1em",
                                "margin": "0 auto",
                                "maxWidth": "90%",
                            }
                        },
                        f"Name of ID {id_value} is: {name}",
                    )
                    if name
                    else None
                ),
                (
                    html.p(
                        {"style": {"color": "#e53e3e", "fontWeight": "bold"}},
                        error,
                    )
                    if error
                    else None
                ),
            ),
        ),
    )

reactpy.run(NameLookupApp, host="0.0.0.0", port=4000)