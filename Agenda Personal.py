import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Asegúrate de tener instalado tkcalendar (pip install tkcalendar)

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("700x400")

        # -------------------------------------------------
        # Frame para la visualización de eventos (TreeView)
        # -------------------------------------------------
        self.frame_eventos = tk.Frame(root, padx=10, pady=10)
        self.frame_eventos.pack(fill=tk.BOTH, expand=True)

        # Configuración del TreeView con columnas para Fecha, Hora y Descripción
        self.tree = ttk.Treeview(self.frame_eventos, columns=("Fecha", "Hora", "Descripción"), show='headings')
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------
        # Frame para la entrada de datos (Fecha, Hora y Descripción)
        # -------------------------------------------------
        self.frame_input = tk.Frame(root, pady=10)
        self.frame_input.pack()

        # Etiqueta y DateEntry para seleccionar la fecha
        tk.Label(self.frame_input, text="Fecha:").grid(row=0, column=0, padx=5)
        self.date_entry = DateEntry(self.frame_input, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5)

        # Etiqueta y Entry para ingresar la hora en formato HH:MM
        tk.Label(self.frame_input, text="Hora (HH:MM):").grid(row=0, column=2, padx=5)
        self.hour_entry = tk.Entry(self.frame_input, width=15)
        self.hour_entry.grid(row=0, column=3, padx=5)

        # Etiqueta y Entry para la descripción del evento
        tk.Label(self.frame_input, text="Descripción:").grid(row=0, column=4, padx=5)
        self.desc_entry = tk.Entry(self.frame_input, width=30)
        self.desc_entry.grid(row=0, column=5, padx=5)

        # -------------------------------------------------
        # Frame para los botones de acción
        # -------------------------------------------------
        self.frame_botones = tk.Frame(root, pady=10)
        self.frame_botones.pack()

        # Botón para agregar un evento
        self.add_btn = tk.Button(self.frame_botones, text="Agregar Evento", command=self.agregar_evento)
        self.add_btn.grid(row=0, column=0, padx=10)

        # Botón para eliminar el evento seleccionado (con confirmación)
        self.del_btn = tk.Button(self.frame_botones, text="Eliminar Evento Seleccionado", command=self.eliminar_evento)
        self.del_btn.grid(row=0, column=1, padx=10)

        # Botón para salir de la aplicación
        self.exit_btn = tk.Button(self.frame_botones, text="Salir", command=self.root.quit)
        self.exit_btn.grid(row=0, column=2, padx=10)

    def validar_hora(self, hora):
        """
        Valida que el formato de la hora sea HH:MM y que los valores sean correctos
        para evitar que se ingresen horas fuera de rango.
        """
        try:
            partes = hora.split(":")
            if len(partes) != 2:
                return False
            h, m = int(partes[0]), int(partes[1])
            return 0 <= h <= 23 and 0 <= m <= 59
        except ValueError:
            return False

    def agregar_evento(self):
        """Agrega un nuevo evento a la agenda después de validar los datos."""
        fecha = self.date_entry.get()
        hora = self.hour_entry.get()
        desc = self.desc_entry.get()

        # Verifica que ningún campo esté vacío
        if not (fecha and hora and desc):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        # Valida el formato y rango de la hora
        if not self.validar_hora(hora):
            messagebox.showwarning(
                "Formato de hora inválido",
                "Por favor, ingresa una hora válida en formato HH:MM."
            )
            return

        # Insertar el nuevo evento en el TreeView
        self.tree.insert("", tk.END, values=(fecha, hora, desc))
        # Limpiar los campos de entrada
        self.hour_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def eliminar_evento(self):
        """Elimina el evento seleccionado luego de confirmar."""
        seleccion = self.tree.selection()
        if seleccion:
            if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar el evento seleccionado?"):
                self.tree.delete(seleccion)
        else:
            messagebox.showwarning("Seleccionar evento", "Selecciona un evento para eliminar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
