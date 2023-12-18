import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter import ttk
import os
from io import BytesIO
import base64
import shutil
from pyexcel_ods3 import save_data


class MedicamentosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Medicamentos")
        self.root.config(bg="#009FBB")
        self.root.resizable(False, False)
        self.imagen_tk = None
        self.editar_imagen_path = tk.StringVar()
        self.editar_imagen_path.set("")
        self.entry_busqueda = tk.Entry(root, width=30)
        self.entry_busqueda.grid(
            row=1, column=0, columnspan=2, ipadx=400, ipady=10, pady=(5, 0)
        )
        self.entry_busqueda.bind("<KeyRelease>", self.realizar_busqueda)
        self.form_label_frame = tk.LabelFrame(
            self.root,
            text="Medicamento Formulario",
            bg="#666",
            fg="#f5f5f5",
            font=("open sans", 25, "bold"),
            height=800,
            width=300,
            border="20",
        )
        self.form_label_frame.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.botones_label_frame = tk.LabelFrame(
            self.root,
            text="Acciones",
            bg="#666",
            fg="#f5f5f5",
            font=("open sans", 15, "bold"),
            height=800,
            width=300,
            border="20",
        )
        self.botones_label_frame.grid(row=0, column=1, padx=15, pady=10, sticky="e")
        # mensaje de la busqueda

        self.style = ttk.Style()
        self.style.configure(
            "TButton",
            foreground="blue",
            font=("Arial", 8),
            padding=(2, 5, 2, 5),
            width=20,
        )
        self.style.theme_use(
            "default"
        )  # Necesario para evitar errores en algunos sistemas operativos
        self.style.configure(
            "Treeview.Heading",
            background="#666",
            foreground="#f5f5f5",
            font=("verdana", 12, "bold"),
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", "#666"), ("!active", "#666")],
            foreground=[("active", "#f5f5f5"), ("!active", "#f5f5f5")],
        )
        # Agregar marcador de posición
        self.placeholder_text = "Ingrese su búsqueda aquí"
        self.entry_busqueda.insert(0, self.placeholder_text)
        self.entry_busqueda.config(fg="grey")
        self.entry_busqueda.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_busqueda.bind("<FocusOut>", self.on_entry_focus_out)
        self.entry_busqueda.bind("<KeyRelease>", self.realizar_busqueda)

        # Crear la base de datos SQLite y la tabla
        self.conn = sqlite3.connect("db.sqlite")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS medicamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                composicion TEXT,
                laboratorio TEXT,
                cantidad INTEGER,
                imagen_path TEXT
            )
        """
        )
        self.conn.commit()

        # Crear la carpeta 'assert' para almacenar imágenes
        if not os.path.exists("assert"):
            os.makedirs("assert")

        # Variables de entrada
        self.entry_nombre = tk.Text(root, height=1, width=30)
        self.entry_composicion = tk.Text(root, width=30)
        self.entry_laboratorio = tk.Text(root, height=1, width=30)
        self.entry_cantidad = tk.Text(root, height=1, width=30)
        self.entry_imagen_path = tk.StringVar()
        self.entry_imagen_path.set("")

        # Configurar la interfaz gráfica llamando a métodos de instancia
        self.configurar_formulario()
        self.configurar_treeview()
        self.configurar_botones()

    def descargar_ods(self):
        try:
            # Obtener todos los datos de la base de datos
            self.cursor.execute("SELECT * FROM medicamentos")
            datos = self.cursor.fetchall()

            # Verificar si hay datos antes de continuar
            if not datos:
                messagebox.showinfo("No hay datos", "No hay datos para descargar.")
                return
            # Mostrar el cuadro de diálogo para seleccionar la ubicación del archivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".ods",
                filetypes=[("ODS files", "*.ods")],
                title="Guardar como ODS",
            )

            hoja_calculo = {
                "Medicamentos": [
                    [
                        "ID",
                        "Nombre",
                        "Composición",
                        "Laboratorio",
                        "Cantidad",
                        "Imagen",
                    ],
                    *datos,
                ]
            }

            save_data(file_path, hoja_calculo)

            messagebox.showinfo(
                "Descarga Exitosa", "Datos descargados como ODS correctamente."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar ODS: {str(e)}")

    def on_entry_focus_in(self, event):
        if self.entry_busqueda.get() == self.placeholder_text:
            self.entry_busqueda.delete(0, tk.END)
            self.entry_busqueda.config(fg="black")

    def on_entry_focus_out(self, event):
        if not self.entry_busqueda.get():
            self.entry_busqueda.insert(0, self.placeholder_text)
            self.entry_busqueda.config(fg="grey")

    def realizar_busqueda(self, event):
        valor_busqueda = self.entry_busqueda.get()
        if valor_busqueda != self.placeholder_text:
            # Realizar la búsqueda aquí
            print("Búsqueda:", valor_busqueda)

    def configurar_formulario(self):
        tk.Label(
            self.form_label_frame,
            text="Nombre",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=0, column=0, sticky="w", padx=6, pady=10)

        tk.Label(
            self.form_label_frame,
            text="Composición",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=1, column=0, sticky="w", padx=6, pady=10)
        tk.Label(
            self.form_label_frame,
            text="Laboratorio",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=2, column=0, sticky="w", padx=6, pady=10)
        tk.Label(
            self.form_label_frame,
            text="Cantidad",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=3, column=0, sticky="w", padx=6, pady=10)
        tk.Label(
            self.form_label_frame,
            text="Imagen",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=4, column=0, sticky="w", padx=6, pady=10)

        self.entry_nombre = tk.Text(self.form_label_frame, height=1, width=30)
        self.entry_composicion = tk.Text(self.form_label_frame, height=3, width=30)
        self.entry_laboratorio = tk.Text(self.form_label_frame, height=1, width=30)
        self.entry_cantidad = tk.Text(self.form_label_frame, height=1, width=30)
        self.entry_imagen_path = tk.StringVar()
        self.entry_imagen_path.set("")

        tk.Button(
            self.form_label_frame,
            text="Guardar",
            command=self.insertar_datos,
            font=("arial", 13, "bold"),
            relief="flat",
            width=25,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=5, column=0, columnspan=3, pady=9, padx=12, ipady=2)

        self.entry_nombre.grid(row=0, column=1, sticky="w", padx=30)
        self.entry_composicion.grid(row=1, column=1, sticky="w", padx=30)
        self.entry_laboratorio.grid(row=2, column=1, sticky="w", padx=30)
        self.entry_cantidad.grid(
            row=3,
            column=1,
            sticky="w",
            padx=30,
        )
        tk.Entry(
            self.form_label_frame,
            textvariable=self.entry_imagen_path,
            state="disabled",
            width=30,
        ).grid(row=4, column=1, sticky="w", padx=90)
        ttk.Button(
            self.form_label_frame,
            text="Seleccionar Imagen",
            command=self.seleccionar_imagen,
        ).grid(row=4, column=1, sticky="w", padx=30)

    def configurar_treeview(self):
        self.treeview = ttk.Treeview(
            self.root,
            columns=(1, 2, 3, 4, 5),
            show="headings",
            height=10,
            takefocus=None,
        )
        self.treeview.grid(row=6, column=0, columnspan=3)

        self.treeview.heading(1, text="ID")
        self.treeview.heading(2, text="Nombre")
        self.treeview.heading(3, text="Composición")
        self.treeview.heading(4, text="Laboratorio")
        self.treeview.heading(5, text="Cantidad")
        self.treeview.tag_configure("oddrow", background="#f0f0f0")
        self.treeview.tag_configure("evenrow", background="#ffffff")
        scrollbar = ttk.Scrollbar(
            self.root, orient="vertical", command=self.treeview.yview
        )
        scrollbar.grid(row=6, column=2, sticky="ns")

        # Configurar el Treeview para usar el Scrollbar
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Configurar el ancho de las columnas y centrar el texto
        for col in range(1, 6):
            self.treeview.column(
                col, anchor="center"
            )  # Ajusta el ancho según sea necesario

        self.mostrar_datos()

    def configurar_botones(self):
        tk.Button(
            self.botones_label_frame,
            text="Eliminar",
            command=self.eliminar_medicamento,
            font=("arial", 13, "bold"),
            relief="flat",
            width=20,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=0, column=0, pady=5)
        tk.Button(
            self.botones_label_frame,
            text="Actualizar",
            command=self.abrir_ventana_actualizar,
            font=("arial", 13, "bold"),
            relief="flat",
            width=20,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=1, column=0, pady=5)
        tk.Button(
            self.botones_label_frame,
            text="Ver",
            command=self.seleccionar_medicamento,
            font=("arial", 13, "bold"),
            relief="flat",
            width=20,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=2, column=0, pady=5)
        tk.Button(
            self.botones_label_frame,
            text="Cerrar",
            command=self.cerrar_aplicacion,
            font=("arial", 13, "bold"),
            relief="flat",
            width=20,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=3, column=0, pady=5, sticky="s")

        tk.Button(
            self.botones_label_frame,
            text="Descargar Excel",
            command=self.descargar_ods,
            font=("arial", 13, "bold"),
            relief="flat",
            width=20,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=4, column=0, pady=5)

    def realizar_busqueda(self, event):
        valor_busqueda = self.entry_busqueda.get().strip().lower()
        # Limpiar el treeview antes de realizar la búsqueda
        self.treeview.delete(*self.treeview.get_children())
        self.treeview.tag_configure(
            "mensaje", background="#ffcccc", foreground="#ff0000"
        )  # Estilo para el mensaje

        self.cursor.execute("SELECT * FROM medicamentos")
        medicamentos = self.cursor.fetchall()

        resultados = []
        for medicamento in medicamentos:
            if valor_busqueda in str(medicamento).lower():
                resultados.append(medicamento)
                pass
        if not resultados:
            # No se encontraron resultados, mostrar mensaje en el treeview
            self.treeview.insert(
                "",
                "end",
                values=("No se encontraron resultados", "", "", "", ""),
                tags=("mensaje",),
            )

        else:
            # Se encontraron resultados, mostrar en el treeview
            for medicamento in resultados:
                self.treeview.insert("", "end", values=medicamento)
                pass

        # Aplicar etiquetas a las filas
        self.treeview.tag_configure("oddrow", background="#777", foreground="#f3f3f3")
        self.treeview.tag_configure("evenrow", background="#e2cfcf", foreground="#666")
        self.treeview.tag_configure(
            "mensaje", background="#ffcccc", foreground="#ff0000"
        )  # Estilo para el mensaje

    def abrir_ventana_actualizar(self):
        item = self.treeview.selection()

        if item:
            item_id = self.treeview.item(item, "values")[0]
            self.ventana_actualizar = tk.Toplevel(self.root)
            self.ventana_actualizar.resizable(False, False)
            self.ventana_actualizar.config(bg="#666")
            self.ventana_actualizar.title("Actualizar Medicamento")

            self.configurar_formulario_actualizar(item_id)

    def configurar_formulario_actualizar(self, item_id):
        self.entry_nombre_actualizar = tk.Text(
            self.ventana_actualizar, height=1, width=30
        )
        self.entry_composicion_actualizar = tk.Text(
            self.ventana_actualizar, height=3, width=30
        )
        self.entry_laboratorio_actualizar = tk.Text(
            self.ventana_actualizar, height=1, width=30
        )
        self.entry_cantidad_actualizar = tk.Text(
            self.ventana_actualizar, height=1, width=30
        )
        self.entry_imagen_path_actualizar = tk.StringVar()

        self.cursor.execute("SELECT * FROM medicamentos WHERE id=?", (item_id,))
        medicamento = self.cursor.fetchone()

        if medicamento:
            self.entry_nombre_actualizar.insert(tk.END, medicamento[1])
            self.entry_composicion_actualizar.insert(tk.END, medicamento[2])
            self.entry_laboratorio_actualizar.insert(tk.END, medicamento[3])
            self.entry_cantidad_actualizar.insert(tk.END, medicamento[4])
            self.entry_imagen_path_actualizar.set(medicamento[5])

        tk.Label(
            self.ventana_actualizar,
            text="Nombre",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(
            self.ventana_actualizar,
            text="Composición",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(
            self.ventana_actualizar,
            text="Laboratorio",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(
            self.ventana_actualizar,
            text="Cantidad",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=3, column=0, sticky="w", pady=5)
        tk.Label(
            self.ventana_actualizar,
            text="Imagen",
            bg="#666",
            fg="#f5f5f5",
            font=("verdana", 12),
        ).grid(row=4, column=0, sticky="w", pady=5)

        self.entry_nombre_actualizar.grid(row=0, column=1, sticky="w")
        self.entry_composicion_actualizar.grid(row=1, column=1, sticky="w")
        self.entry_laboratorio_actualizar.grid(row=2, column=1, sticky="w")
        self.entry_cantidad_actualizar.grid(row=3, column=1, sticky="w")
        tk.Entry(
            self.ventana_actualizar,
            textvariable=self.entry_imagen_path_actualizar,
            state="disabled",
            width=20,
        ).grid(row=4, column=1, sticky="w", padx=105)
        tk.Button(
            self.ventana_actualizar,
            text="Seleccionar Imagen",
            command=self.seleccionar_imagen_actualizar,
        ).grid(row=4, columns=1, columnspan=3, padx=110, sticky="w")
        tk.Button(
            self.ventana_actualizar,
            text="Actualizar",
            command=lambda: self.guardar_actualizacion(item_id),
            font=("arial", 13, "bold"),
            relief="flat",
            width=25,
            foreground="#f5f5f5",
            background="#009FBB",
            border="10",
        ).grid(row=5, column=0, columnspan=3)

    def seleccionar_imagen_actualizar(self):
        file_path = filedialog.askopenfilename()
        self.entry_imagen_path_actualizar.set(file_path)

    def guardar_actualizacion(self, item_id):
        nombre = self.entry_nombre_actualizar.get("1.0", tk.END).strip()
        composicion = self.entry_composicion_actualizar.get("1.0", tk.END).strip()
        laboratorio = self.entry_laboratorio_actualizar.get("1.0", tk.END).strip()
        cantidad = self.entry_cantidad_actualizar.get("1.0", tk.END).strip()
        imagen_path = self.entry_imagen_path_actualizar.get()

        # Guardar la imagen en la carpeta 'assert'
        if imagen_path:
            nombre_imagen = os.path.basename(imagen_path)
            nueva_ruta = os.path.join("assert", nombre_imagen)
            # Verificar si la ruta de origen y destino son distintas antes de copiar
            if imagen_path != nueva_ruta:
                shutil.copy(imagen_path, nueva_ruta)
                imagen_path = nueva_ruta

        self.cursor.execute(
            """
            UPDATE medicamentos 
            SET nombre=?, composicion=?, laboratorio=?, cantidad=?, imagen_path=? 
            WHERE id=?
            """,
            (nombre, composicion, laboratorio, cantidad, imagen_path, item_id),
        )
        self.conn.commit()
        self.mostrar_datos()
        self.ventana_actualizar.destroy()

    def insertar_datos(self):
        nombre = self.entry_nombre.get("1.0", tk.END).strip()
        composicion = self.entry_composicion.get("1.0", tk.END).strip()
        laboratorio = self.entry_laboratorio.get("1.0", tk.END).strip()
        cantidad = self.entry_cantidad.get("1.0", tk.END).strip()
        imagen_path = self.entry_imagen_path.get()

        if (
            not nombre
            or not composicion
            or not laboratorio
            or not cantidad
            or not imagen_path
        ):
            messagebox.showwarning(
                "Campos Vacíos", "Por favor, llene todos los campos antes de guardar."
            )
        else:
            # Guardar la imagen en la carpeta 'assert'
            if imagen_path:
                nombre_imagen = os.path.basename(imagen_path)
                nueva_ruta = os.path.join("assert", nombre_imagen)
                shutil.copy(imagen_path, nueva_ruta)
                imagen_path = nueva_ruta

            self.cursor.execute(
                "INSERT INTO medicamentos (nombre, composicion, laboratorio, cantidad, imagen_path) VALUES (?, ?, ?, ?, ?)",
                (nombre, composicion, laboratorio, cantidad, imagen_path),
            )
            self.conn.commit()
            self.mostrar_datos()

            # Limpiar campos después de guardar
            self.entry_nombre.delete("1.0", tk.END)
            self.entry_composicion.delete("1.0", tk.END)
            self.entry_laboratorio.delete("1.0", tk.END)
            self.entry_cantidad.delete("1.0", tk.END)
            self.entry_imagen_path.set("")

    def mostrar_datos(self):
        self.treeview.delete(*self.treeview.get_children())
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        self.cursor.execute("SELECT * FROM medicamentos")
        medicamentos = self.cursor.fetchall()

        if not medicamentos:
            self.treeview.insert(
                "",
                "end",
                values=("No hay medicamentos registrado", "", "", "", ""),
                tags=("mensaje",),
            )

        # else:
        #     self.estado_label.config(text='')

        for index, medicamento in enumerate(medicamentos):
            tag = "oddrow" if index % 2 == 1 else "evenrow"
            self.treeview.insert("", "end", values=medicamento, tags=(tag,))

        # Aplicar etiquetas a las filas
        self.treeview.tag_configure("oddrow", background="#777", foreground="#f3f3f3")
        self.treeview.tag_configure("evenrow", background="#e2cfcf", foreground="#666")

    def seleccionar_medicamento(self):
        item = self.treeview.selection()
        if item:
            # Obtener el primer elemento de la selección
            item_id = self.treeview.item(item[0], "values")[0]
            self.detalle_medicamento(item_id)

    def detalle_medicamento(self, item):
        detalle_window = tk.Toplevel(self.root)
        detalle_window.title("Detalles del Medicamento")
        detalle_window.resizable(False, False)
        detalle_window.geometry("380x590")
        detalle_window.config(bg="#009FBB")

        # Si item es una tupla, obtén el primer elemento (ID del medicamento)
        item_id = item[0] if isinstance(item, tuple) else item

        self.cursor.execute("SELECT * FROM medicamentos WHERE id=?", (item_id,))
        medicamento = self.cursor.fetchone()

        if medicamento:
            for i, campo in enumerate(
                ["ID", "Nombre", "Composición", "Laboratorio", "Cantidad"]
            ):
                tk.Label(
                    detalle_window,
                    text=campo,
                    font=("open sans", 15, "bold"),
                    bg="#009FBB",
                    fg="#f5f5f5",
                ).grid(row=i, column=0, sticky="w", pady=8)

                # Verificar si el valor es None antes de intentar acceder al índice
                valor = medicamento[i]
                if valor is not None:
                    tk.Label(
                        detalle_window,
                        text=valor,
                        font=("open sans", 15, "bold"),
                        bg="#009FBB",
                        fg="#f5f5f5",
                    ).grid(row=i, column=1, sticky="w")
                else:
                    tk.Label(
                        detalle_window,
                        text="N/A",
                        font=("open sans", 15, "bold"),
                        bg="#009FBB",
                        fg="#f5f5f5",
                    ).grid(row=i, column=1, sticky="w")

            imagen_path = medicamento[5]

            # Verificar si la ruta de la imagen no es None antes de intentar abrir la imagen
            if imagen_path is not None:
                imagen = Image.open(imagen_path)
                imagen.thumbnail((500, 200))
                self.imagen_tk = ImageTk.PhotoImage(imagen)

                # tk.Label(
                #     detalle_window,
                #     text="Imagen",
                #     font=("open sans", 15, "bold"),
                #     bg="#009FBB",
                #     fg="#f5f5f5",
                # ).grid(row=5, column=0, sticky="w")
                tk.Label(
                    detalle_window,
                    image=self.imagen_tk,
                    bg="#009FBB",
                    anchor="center",
                    width=300,
                    height=300,
                ).grid(row=5, padx=20, sticky="w", columnspan=2)

                # Configurar la columna y fila para que se expanda con el tamaño de la ventana

                tk.Button(
                    detalle_window,
                    text="Cerrar",
                    command=detalle_window.destroy,
                    font=("open sans", 15, "bold"),
                    relief="flat",
                    width=30,
                    foreground="#009FBB",
                    background="#f5f5f5",
                    border="10",
                    justify="center",
                ).grid(row=6, column=0, columnspan=2)
            else:
                tk.Label(
                    detalle_window,
                    text="N/A",
                    font=("open sans", 15, "bold"),
                    bg="#009FBB",
                    fg="#f5f5f5",
                ).grid(row=5, column=0, sticky="w")

                tk.Button(
                    detalle_window,
                    text="Cerrar",
                    command=detalle_window.destroy,
                    font=("open sans", 15, "bold"),
                    relief="flat",
                    width=30,
                    foreground="#009FBB",
                    background="#f5f5f5",
                    border="10",
                    justify="center",
                ).grid(row=5, column=0, columnspan=2)
        else:
            tk.Label(
                detalle_window,
                text="No se encontraron detalles para este medicamento",
                font=("open sans", 15, "bold"),
                bg="#009FBB",
                fg="#f5f5f5",
            ).grid(row=0, column=0, columnspan=2)
            tk.Button(
                detalle_window,
                text="Cerrar",
                command=detalle_window.destroy,
                font=("open sans", 15, "bold"),
                relief="flat",
                width=20,
                foreground="#009FBB",
                background="#f5f5f5",
                border="10",
            ).grid(row=4, column=0, columnspan=2, pady=10)

    def eliminar_medicamento(self):
        item = self.treeview.selection()
        if item:
            item_id = self.treeview.item(item, "values")[0]
            confirmacion = messagebox.askokcancel(
                "Confirmar", "¿Estás seguro de que quieres eliminar este medicamento?"
            )
            if confirmacion:
                self.cursor.execute("DELETE FROM medicamentos WHERE id=?", (item_id,))
                self.conn.commit()
                self.mostrar_datos()

    def cerrar_aplicacion(self):
        confirmacion = messagebox.askokcancel(
            "Confirmar", "¿Estás seguro de que quieres cerrar la aplicación?"
        )
        if confirmacion:
            self.root.destroy()

    def seleccionar_imagen(self):
        file_path = filedialog.askopenfilename()
        self.entry_imagen_path.set(file_path)

    def run(self):
        # Método para ejecutar la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.mostrar_datos()
        self.root.mainloop()

    def __del__(self):
        # Método para cerrar la conexión a la base de datos al salir
        self.conn.close()


# Crear una instancia de la clase MedicamentosApp y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    # root.configure(bg='#666')

    app = MedicamentosApp(root)

    app.run()
