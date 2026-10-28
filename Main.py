import tkinter as tk
from tkinter import ttk
import math
import random
import json

class RunwaySimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aerospace CV Runway Detector Simulation (Zero-Pip)")
        self.root.geometry("800x600")
        
        self.fog_density = tk.DoubleVar(value=0.0)
        self.history = {}
        
        self.setup_ui()
        self.update_simulation()

    def setup_ui(self):
        header = tk.Label(self.root, text="Runway Detection Weather Degradation Model", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        self.canvas = tk.Canvas(self.root, width=640, height=360, bg="#87CEEB") # Sky blue baseline
        self.canvas.pack(pady=10)
        
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill="x", padx=50, pady=10)
        
        slider_label = tk.Label(control_frame, text="Simulated Fog Density (%):", font=("Arial", 11))
        slider_label.grid(row=0, column=0, sticky="w")
        
        self.slider = ttk.Scale(control_frame, from_=0, to=100, variable=self.fog_density, 
                                 orient="horizontal", command=lambda e: self.update_simulation())
        self.slider.grid(row=0, column=1, sticky="ew", padx=10)
        
        self.val_label = tk.Label(control_frame, text="0%", font=("Arial", 11, "bold"), width=6)
        self.val_label.grid(row=0, column=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        self.metrics_label = tk.Label(self.root, text="Status: Initializing...", font=("Courier", 12), fg="blue")
        self.metrics_label.pack(pady=5)
        
        self.btn_run = tk.Button(self.root, text="🚀 Run Automated Bootcamp Experiment", 
                                 font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", 
                                 command=self.run_full_experiment, padx=10, pady=5)
        self.btn_run.pack(pady=10)

    def draw_environment(self, fog_val):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(0, 180, 640, 360, fill="#556B2F", outline="")
        self.canvas.create_rectangle(0, 0, 640, 180, fill="#a0c4de", outline="")
        
        gt_coords = [300, 180, 340, 180, 480, 360, 160, 360]
        
        runway_base_rgb = (40, 40, 40)
        fog_rgb = (220, 220, 220)
        
        extinction = (fog_val / 100.0) * 2.5
        contrast_factor = math.exp(-extinction)
        
        r = int(runway_base_rgb[0] * contrast_factor + fog_rgb[0] * (1 - contrast_factor))
        g = int(runway_base_rgb[1] * contrast_factor + fog_rgb[1] * (1 - contrast_factor))
        b = int(runway_base_rgb[2] * contrast_factor + fog_rgb[2] * (1 - contrast_factor))
        runway_color = f"#{r:02x}{g:02x}{b:02x}"
        
        self.canvas.create_polygon(gt_coords, fill=runway_color, outline="")
        
        sensor_signal = 1.0 * contrast_factor
        noise = random.uniform(-0.06, 0.06)
        effective_signal = sensor_signal + noise
        
        cv_detection_threshold = 0.18 
        
        if effective_signal >= cv_detection_threshold:
            deviation = (1.0 - contrast_factor) * 45
            pred_coords = [
                gt_coords[0] + random.uniform(-deviation*0.2, deviation*0.2),
                gt_coords[1],
                gt_coords[2] + random.uniform(-deviation*0.2, deviation*0.2),
                gt_coords[3],
                gt_coords[4] + random.uniform(-deviation, deviation),
                gt_coords[5],
                gt_coords[6] + random.uniform(-deviation, deviation),
                gt_coords[7]
            ]
            self.canvas.create_polygon(pred_coords, fill="", outline="#00FF00", width=3, dash=(4, 4))
            
            iou = max(0.0, min(1.0, contrast_factor - (abs(noise) * 2)))
            status_text = f"TRACK LOCKED | Sensor Signal: {sensor_signal:.2f} | Target IoU: {iou:.2%}"
            status_color = "green"
        else:
            iou = 0.0
            status_text = "CRITICAL ALERT: SENSOR BLINDOUT | Target Lost (IoU: 0.00%)"
            status_color = "red"
            
        fog_hex = f"#{int(fog_rgb[0]):02x}{int(fog_rgb[1]):02x}{int(fog_rgb[2]):02x}"
        if fog_val > 5:
            spacing = max(2, int(15 - (fog_val / 8)))
            for y in range(0, 360, spacing):
                self.canvas.create_line(0, y, 640, y, fill=fog_hex, width=int(fog_val/20)+1)

        return status_text, status_color, iou

    def update_simulation(self):
        val = int(self.fog_density.get())
        self.val_label.config(text=f"{val}%")
        
        txt, color, _ = self.draw_environment(val)
        self.metrics_label.config(text=txt, fg=color)

    def run_full_experiment(self):
        """Simulates 100 approaches at key intervals to map the threshold curve."""
        test_points = [0, 20, 40, 55, 70, 90, 100]
        runs_per_point = 50
        self.history = {}
        
        print("\n--- Running Automated Batch Analysis ---")
        for p in test_points:
            successes = 0
            for _ in range(runs_per_point):
                c_factor = math.exp(-(p / 100.0) * 2.5)
                if (c_factor + random.uniform(-0.06, 0.06)) >= 0.18:
                    successes += 1
            
            acc = (successes / runs_per_point) * 100
            label = f"{p}% Fog"
            self.history[label] = f"{acc}%"
            print(f"Tested Fog Level: {p}% | CV Accuracy: {acc}%")
            
        with open("bootcamp_experiment_results.json", "w") as f:
            json.dump(self.history, f, indent=4)
            
        self.metrics_label.config(
            text="Experiment Complete! Results saved to 'bootcamp_experiment_results.json'", 
            fg="purple"
        )

if __name__ == "__main__":
    random.seed(42)
    root = tk.Tk()
    app = RunwaySimulationApp(root)
    root.mainloop()