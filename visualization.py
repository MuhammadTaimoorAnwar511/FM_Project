import tkinter as tk
from tkinter import ttk

def create_checkbox_tree(feature_model):
    root = tk.Tk()
    root.title("Feature Model Visualization")
    tree = ttk.Treeview(root)
    tree.pack()

    def add_feature(node, feature):
        feature_id = tree.insert(node, 'end', text=feature['name'])
        for child in feature.get('children', []):
            add_feature(feature_id, child)
        for group in feature.get('groups', []):
            group_id = tree.insert(feature_id, 'end', text=f"{group['type']} group")
            for gf in group['features']:
                add_feature(group_id, gf)

    add_feature('', feature_model['root'])
    root.mainloop()
