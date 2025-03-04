import os

def save_graph_image(graph, name: str = "multi_agent_graph.png"):
    try:
        os.makedirs(os.path.join("data", "graphs"), exist_ok=True)
        output_path = os.path.join("data", "graphs", name)

        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        
        with open(output_path, 'wb') as f:
            f.write(png_data)
            
        print(f"Graph visualization saved to: {output_path}")
        
    except Exception as e:
        print(f"Error saving graph visualization: {e}")