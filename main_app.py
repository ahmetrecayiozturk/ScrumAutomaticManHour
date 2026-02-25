import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import json
import pandas as pd

from inference_pipeline import run_pipeline
from capacity_checker import TeamConfig
from fine_tuner import append_sprint_history_by_taskkey, train_adjustments, save_config_updates

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class EstimatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Scrum Automation App")
        self.geometry("600x500")

        self.sprint_file_path = None
        self.actuals_file_path = None

        self.title_label = ctk.CTkLabel(self, text="Scrum Automation App", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        self.frame_estimate = ctk.CTkFrame(self)
        self.frame_estimate.pack(pady=10, padx=20, fill="x")
        
        self.lbl_estimate = ctk.CTkLabel(self.frame_estimate, text="1. Yeni Sprint Tahmini Oluştur", font=ctk.CTkFont(weight="bold"))
        self.lbl_estimate.pack(pady=10)

        self.btn_select_sprint = ctk.CTkButton(self.frame_estimate, text="Sprint Excel'i Seç", command=self.select_sprint_file)
        self.btn_select_sprint.pack(pady=5)

        self.lbl_sprint_path = ctk.CTkLabel(self.frame_estimate, text="Dosya seçilmedi", text_color="gray")
        self.lbl_sprint_path.pack(pady=5)

        self.btn_run_pipeline = ctk.CTkButton(self.frame_estimate, text="Tahminleri Çalıştır", fg_color="green", hover_color="darkgreen", command=self.run_estimation)
        self.btn_run_pipeline.pack(pady=10)

        self.frame_train = ctk.CTkFrame(self)
        self.frame_train.pack(pady=10, padx=20, fill="x")

        self.lbl_train = ctk.CTkLabel(self.frame_train, text="2. Sprint Sonu Modeli Eğit (Kalibrasyon)", font=ctk.CTkFont(weight="bold"))
        self.lbl_train.pack(pady=10)

        self.btn_select_actuals = ctk.CTkButton(self.frame_train, text="Gerçekleşen (Actuals) Excel'i Seç", command=self.select_actuals_file)
        self.btn_select_actuals.pack(pady=5)

        self.lbl_actuals_path = ctk.CTkLabel(self.frame_train, text="Dosya seçilmedi", text_color="gray")
        self.lbl_actuals_path.pack(pady=5)

        self.btn_train_model = ctk.CTkButton(self.frame_train, text="Modeli Eğit", fg_color="orange", hover_color="darkorange", command=self.train_model)
        self.btn_train_model.pack(pady=10)

    def select_sprint_file(self):
        filetypes = (("Excel files", "*.xlsx"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title="Sprint Excel Seç", filetypes=filetypes)
        if filepath:
            self.sprint_file_path = filepath
            self.lbl_sprint_path.configure(text=os.path.basename(filepath), text_color="white")

    def run_estimation(self):
        if not self.sprint_file_path:
            messagebox.showwarning("Uyarı", "Lütfen önce bir Sprint Excel dosyası seçin!")
            return

        try:
            team = TeamConfig(backend_developers=3, frontend_developers=1, velocity_multiplier=1.15, hours_per_day=6, sprint_days=14)
            
            if os.path.exists("estimated_output.xlsx"): os.remove("estimated_output.xlsx")
            if os.path.exists("estimated_output.json"): os.remove("estimated_output.json")

            result = run_pipeline(
                excel_path=self.sprint_file_path,
                sheet_name="Calculations",
                export_excel_path="estimated_output.xlsx",
                export_json_path="estimated_output.json",
                config_json_path="estimation_config.json",
                team=team
            )
            ###sheet_name="Calculations" yazısını sheet_name=None olarak değiştirirsek
            ### excel şablonunun sayfa adı ne olursa olsun sistem otomatik olarak ilk sayfayı bulup okuyacaktır. bu da bize şunu sağlar:
            # projenin en güzel yanlarından biri bu. Yazdığımız excel_parser.py dosyası o kadar esnek ki, gönderdiğimiz bu yeni sütun isimlerini neredeyse hiçbir kodu değiştirmeden otomatik olarak tanır
            #   yani başka bir sprint template'inde de çalışacaktır. Sadece o template'teki sütun isimlerinin ALIASES sözlüğündeki isimlerden biriyle benzer olması yeterlidir. Böylece yeni bir template geldiğinde, ya da mevcut template'te ufak bir değişiklik yapıldığında, kodda hiçbir değişiklik yapmadan tahminleme yapmaya devam edebiliriz. Bu da bize büyük bir esneklik ve zaman kazandırır.
            #result = run_pipeline(
            #    excel_path=self.sprint_file_path,
            #    sheet_name= None,
            #    export_excel_path="estimated_output.xlsx",
            #    export_json_path="estimated_output.json",
            #    config_json_path="estimation_config.json",
            #    team=team
            #)
            
            messagebox.showinfo("Başarılı", f"Tahminler başarıyla oluşturuldu!\n\nBE Toplam: {result['totals']['BE']} saat\nFE Toplam: {result['totals']['FE']} saat\n\nDosya 'estimated_output.xlsx' olarak kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Tahmin çalıştırılırken bir hata oluştu:\n{str(e)}")

    def select_actuals_file(self):
        filetypes = (("Excel files", "*.xlsx"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title="Gerçekleşen Excel Seç", filetypes=filetypes)
        if filepath:
            self.actuals_file_path = filepath
            self.lbl_actuals_path.configure(text=os.path.basename(filepath), text_color="white")

    def train_model(self):
        if not self.actuals_file_path:
            messagebox.showwarning("Uyarı", "Lütfen gerçekleşen (actuals) sürelerin olduğu dosyayı seçin!")
            return
        if not os.path.exists("estimated_output.json"):
            messagebox.showwarning("Uyarı", "Geçmiş tahmin verisi (estimated_output.json) bulunamadı. Lütfen önce tahmin çalıştırın.")
            return

        try:
            with open("estimated_output.json", "r", encoding="utf-8") as f:
                estimated_rows = json.load(f)

            df_act = pd.read_excel(self.actuals_file_path, engine="openpyxl")
            actual_rows = df_act.to_dict(orient="records")

            df_all = append_sprint_history_by_taskkey(
                "history.csv",
                estimated_rows,
                actual_rows,
                actual_taskkey_field="TaskKey",
                actual_be_field="Actual_BE",
                actual_fe_field="Actual_FE",
            )

            updates = train_adjustments("history.csv")
            save_config_updates("estimation_config.json", updates)

            messagebox.showinfo("Başarılı", f"Model başarıyla eğitildi!\n\nYeni Katsayılar:\nBE Çarpanı: {updates['adj_be']}\nFE Çarpanı: {updates['adj_fe']}\n\nEğitim veri seti boyutu: {len(df_all)} satır.")
        except Exception as e:
            messagebox.showerror("Hata", f"Model eğitilirken bir hata oluştu:\n{str(e)}")

if __name__ == "__main__":
    app = EstimatorApp()
    app.mainloop()