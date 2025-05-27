import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QGroupBox, QGridLayout, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QBrush
from PyQt5.QtCore import QSize

class DashboardWindow(QWidget):
    """Ventana de dashboard inicial"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.setup_ui()
        self.update_stats()
    
    def setup_ui(self):
        # Crear scroll area principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget contenedor principal
        main_widget = QWidget()
        self.layout = QVBoxLayout(main_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Título mejorado
        title = QLabel("Dashboard - Sistema de Gestión Académica")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            border-radius: 10px;
            border: 2px solid #dee2e6;
        """)
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(80)
        self.layout.addWidget(title)
        
        # Quick Actions mejorado con botones centrados
        quick_actions_group = QGroupBox("⚡ Acciones Rápidas")
        quick_actions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #3498db;
                background-color: #ffffff;
            }
        """)
        quick_actions_group.setFixedHeight(120)  # VOLVER AL TAMAÑO ORIGINAL
        
        # Layout principal para centrar los botones
        quick_actions_main_layout = QVBoxLayout()
        quick_actions_main_layout.setContentsMargins(15, 15, 15, 15)  # VOLVER AL TAMAÑO ORIGINAL
        
        # Layout horizontal para los botones con centrado
        quick_actions_layout = QHBoxLayout()
        quick_actions_layout.setSpacing(12)  # VOLVER AL ESPACIADO ORIGINAL
        
        # Agregar stretch al inicio para centrar
        quick_actions_layout.addStretch()
        
        # Botones de acción centrados CON TAMAÑO ORIGINAL
        self.add_student_btn = self.create_small_action_button("👤 Agregar\nEstudiante", "list-add-user", "#3498db")
        self.add_subject_btn = self.create_small_action_button("📖 Agregar\nAsignatura", "list-add", "#9b59b6")
        self.add_profesor_btn = self.create_small_action_button("👨‍🏫 Agregar\nProfesor", "list-add-user", "#8e44ad")
        self.add_note_btn = self.create_small_action_button("➕ Agregar\nNota", "list-add-document", "#2ecc71")
        
        quick_actions_layout.addWidget(self.add_student_btn)
        quick_actions_layout.addWidget(self.add_subject_btn)
        quick_actions_layout.addWidget(self.add_profesor_btn)
        quick_actions_layout.addWidget(self.add_note_btn)
        
        # Agregar stretch al final para centrar
        quick_actions_layout.addStretch()
        
        # Agregar el layout horizontal al layout principal
        quick_actions_main_layout.addLayout(quick_actions_layout)
        
        quick_actions_group.setLayout(quick_actions_main_layout)
        self.layout.addWidget(quick_actions_group)
        
        # Quick Stats mejorado
        self.quick_stats_group = QGroupBox("📊 Estadísticas Generales")
        self.quick_stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #e74c3c;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #e74c3c;
                background-color: #ffffff;
            }
        """)
        self.quick_stats_group.setFixedHeight(300)
        
        quick_stats_layout = QGridLayout()
        quick_stats_layout.setSpacing(10)
        quick_stats_layout.setContentsMargins(20, 20, 20, 20)
        
        # Crear etiquetas de estadísticas mejoradas
        self.total_estudiantes_label = self.create_stat_label("👨‍🎓 Estudiantes:")
        self.total_asignaturas_label = self.create_stat_label("📚 Asignaturas:")
        self.total_profesores_label = self.create_stat_label("👨‍🏫 Profesores:")
        self.total_notas_label = self.create_stat_label("📝 Notas:")
        self.promedio_general_label = self.create_stat_label("📈 Promedio General:")
        self.estudiantes_riesgo_label = self.create_stat_label("⚠️ Estudiantes en Riesgo:")
        self.mejor_estudiante_label = self.create_stat_label("🏆 Mejor Estudiante:")
        self.peor_estudiante_label = self.create_stat_label("🔻 Peor Estudiante:")
        self.mejor_asignatura_label = self.create_stat_label("🌟 Mejor Asignatura:")
        self.peor_asignatura_label = self.create_stat_label("💢 Peor Asignatura:")
        
        # Organización mejorada en grid 5x2
        quick_stats_layout.addWidget(self.total_estudiantes_label, 0, 0)
        quick_stats_layout.addWidget(self.total_asignaturas_label, 0, 1)
        quick_stats_layout.addWidget(self.total_profesores_label, 1, 0)
        quick_stats_layout.addWidget(self.total_notas_label, 1, 1)
        quick_stats_layout.addWidget(self.promedio_general_label, 2, 0)
        quick_stats_layout.addWidget(self.estudiantes_riesgo_label, 2, 1)
        quick_stats_layout.addWidget(self.mejor_estudiante_label, 3, 0)
        quick_stats_layout.addWidget(self.peor_estudiante_label, 3, 1)
        quick_stats_layout.addWidget(self.mejor_asignatura_label, 4, 0)
        quick_stats_layout.addWidget(self.peor_asignatura_label, 4, 1)
        
        self.quick_stats_group.setLayout(quick_stats_layout)
        self.layout.addWidget(self.quick_stats_group)
        
        # SECCIÓN DE GRÁFICOS COMPLETAMENTE REDISEÑADA
        self.graphs_group = QGroupBox("📈 Visualización de Datos")
        self.graphs_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #f39c12;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #f39c12;
                background-color: #ffffff;
            }
        """)
        # ALTURA FIJA PARA EVITAR SOLAPAMIENTO
        self.graphs_group.setFixedHeight(500)
        
        # Layout principal de gráficos
        graphs_main_layout = QVBoxLayout()
        graphs_main_layout.setContentsMargins(20, 20, 20, 20)
        graphs_main_layout.setSpacing(15)
        
        # Contenedor horizontal para los dos gráficos
        graphs_container = QHBoxLayout()
        graphs_container.setSpacing(20)
        
        # GRÁFICO 1: Distribución de notas
        graph1_frame = QFrame()
        graph1_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        graph1_frame.setFixedSize(400, 350)  # TAMAÑO FIJO
        
        graph1_layout = QVBoxLayout(graph1_frame)
        graph1_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título del gráfico 1
        graph1_title = QLabel("Distribución de Calificaciones")
        graph1_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background: transparent;
                padding: 5px;
            }
        """)
        graph1_title.setAlignment(Qt.AlignCenter)
        graph1_layout.addWidget(graph1_title)
        
        # Canvas del gráfico 1
        self.figure1 = plt.figure(figsize=(5, 4), dpi=80)
        self.figure1.patch.set_facecolor('#f8f9fa')
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setFixedSize(380, 300)  # TAMAÑO FIJO DEL CANVAS
        graph1_layout.addWidget(self.canvas1)
        
        # GRÁFICO 2: Estudiantes en riesgo
        graph2_frame = QFrame()
        graph2_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        graph2_frame.setFixedSize(400, 350)  # TAMAÑO FIJO
        
        graph2_layout = QVBoxLayout(graph2_frame)
        graph2_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título del gráfico 2
        graph2_title = QLabel("Estado Académico de Estudiantes")
        graph2_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background: transparent;
                padding: 5px;
            }
        """)
        graph2_title.setAlignment(Qt.AlignCenter)
        graph2_layout.addWidget(graph2_title)
        
        # Canvas del gráfico 2
        self.figure2 = plt.figure(figsize=(5, 4), dpi=80)
        self.figure2.patch.set_facecolor('#f8f9fa')
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setFixedSize(380, 300)  # TAMAÑO FIJO DEL CANVAS
        graph2_layout.addWidget(self.canvas2)
        
        # Agregar los frames al contenedor horizontal
        graphs_container.addWidget(graph1_frame)
        graphs_container.addWidget(graph2_frame)
        graphs_container.addStretch()  # Espacio flexible al final
        
        # Agregar el contenedor al layout principal de gráficos
        graphs_main_layout.addLayout(graphs_container)
        graphs_main_layout.addStretch()  # Espacio flexible al final
        
        self.graphs_group.setLayout(graphs_main_layout)
        self.layout.addWidget(self.graphs_group)
        
        # Botón para ver todo mejorado y centrado
        button_container = QHBoxLayout()
        button_container.addStretch()  # Stretch al inicio
        self.view_all_btn = self.create_action_button("👁️ Ver Todos los Datos", "document-preview", "#34495e")
        self.view_all_btn.setFixedHeight(60)
        button_container.addWidget(self.view_all_btn)
        button_container.addStretch()  # Stretch al final
        
        self.layout.addLayout(button_container)
        
        # Configurar el scroll area
        scroll_area.setWidget(main_widget)
        
        # Layout principal de la ventana
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        # Aplicar estilo general a la ventana
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QScrollArea {
                border: none;
                background-color: #ecf0f1;
            }
            QScrollBar:vertical {
                background-color: #bdc3c7;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #7f8c8d;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #34495e;
            }
        """)
        
        self.setLayout(main_layout)
        
        # Establecer tamaño mínimo de la ventana
        self.setMinimumSize(900, 700)
    
    def create_stat_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding: 8px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                color: #495057;
                font-weight: 500;
                min-height: 15px;
            }
        """)
        return label
    
    def create_small_action_button(self, text, icon_name, color):
        """Crear botones pequeños para acciones rápidas - TAMAÑO ORIGINAL"""
        button = QPushButton(text)
        button.setIcon(QIcon.fromTheme(icon_name))
        button.setIconSize(QSize(20, 20))  # VOLVER AL TAMAÑO ORIGINAL
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;  /* VOLVER AL TAMAÑO ORIGINAL */
                font-weight: bold;
                font-size: 13px;  /* MANTENER LA LETRA GRANDE */
                background-color: {color};
                color: white;
                border-radius: 8px;  /* VOLVER AL TAMAÑO ORIGINAL */
                min-width: 110px;  /* VOLVER AL TAMAÑO ORIGINAL */
                min-height: 50px;  /* VOLVER AL TAMAÑO ORIGINAL */
                border: none;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
                transform: scale(1.02);
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 20)};
            }}
        """)
        return button
    
    def create_action_button(self, text, icon_name, color):
        """Mantener el botón normal para 'Ver Todos los Datos'"""
        button = QPushButton(text)
        button.setIcon(QIcon.fromTheme(icon_name))
        button.setIconSize(QSize(32, 32))
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 15px;
                font-weight: bold;
                font-size: 13px;
                background-color: {color};
                color: white;
                border-radius: 10px;
                min-width: 140px;
                min-height: 70px;
                border: none;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
                transform: scale(1.02);
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 20)};
            }}
        """)
        return button
    
    def darken_color(self, hex_color, percent=10):
        """Oscurece un color hexadecimal"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def update_stats(self):
        stats = self.sistema.obtener_estadisticas_generales()
        
        # Actualizar etiquetas con estilos mejorados
        self.update_stat_label(self.total_estudiantes_label, f"👨‍🎓 Estudiantes: {stats['total_estudiantes']}")
        self.update_stat_label(self.total_asignaturas_label, f"📚 Asignaturas: {stats['total_asignaturas']}")
        self.update_stat_label(self.total_profesores_label, f"👨‍🏫 Profesores: {len(self.sistema.profesores)}")
        self.update_stat_label(self.total_notas_label, f"📝 Notas: {stats['total_notas']}")
        self.update_stat_label(self.promedio_general_label, f"📈 Promedio General: {stats['promedio_general']:.2f}")
        
        # Color especial para estudiantes en riesgo
        riesgo_text = f"⚠️ Estudiantes en Riesgo: {stats['estudiantes_riesgo']}"
        self.estudiantes_riesgo_label.setText(riesgo_text)
        if stats['estudiantes_riesgo'] > 0:
            self.estudiantes_riesgo_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    padding: 8px;
                    background-color: #f8d7da;
                    border: 2px solid #f5c6cb;
                    border-radius: 6px;
                    color: #721c24;
                    font-weight: bold;
                    min-height: 15px;
                }
            """)
        else:
            self.estudiantes_riesgo_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    padding: 8px;
                    background-color: #d4edda;
                    border: 2px solid #c3e6cb;
                    border-radius: 6px;
                    color: #155724;
                    font-weight: bold;
                    min-height: 15px;
                }
            """)
        
        # Mejor y peor estudiante/asignatura con colores especiales
        self.update_stat_label_special(self.mejor_estudiante_label, 
                                     f"🏆 Mejor: {stats['mejor_estudiante'][0]} ({stats['mejor_estudiante'][1]:.2f})", 
                                     "#d4edda", "#155724")
        self.update_stat_label_special(self.peor_estudiante_label, 
                                     f"🔻 Peor: {stats['peor_estudiante'][0]} ({stats['peor_estudiante'][1]:.2f})", 
                                     "#f8d7da", "#721c24")
        self.update_stat_label_special(self.mejor_asignatura_label, 
                                     f"🌟 Mejor: {stats['mejor_asignatura'][0]} ({stats['mejor_asignatura'][1]:.2f})", 
                                     "#d1ecf1", "#0c5460")
        self.update_stat_label_special(self.peor_asignatura_label, 
                                     f"💢 Peor: {stats['peor_asignatura'][0]} ({stats['peor_asignatura'][1]:.2f})", 
                                     "#ffeaa7", "#6c5ce7")
        
        # Actualizar gráficos
        self.update_charts()
    
    def update_stat_label(self, label, text):
        label.setText(text)
        label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding: 8px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                color: #495057;
                font-weight: 500;
                min-height: 15px;
            }
        """)
    
    def update_stat_label_special(self, label, text, bg_color, text_color):
        label.setText(text)
        label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                padding: 8px;
                background-color: {bg_color};
                border: 2px solid {self.darken_color(bg_color, 15)};
                border-radius: 6px;
                color: {text_color};
                font-weight: bold;
                min-height: 15px;
            }}
        """)
    
    def update_charts(self):
        # Gráfico 1: Distribución de notas mejorado
        self.figure1.clear()
        ax1 = self.figure1.add_subplot(111)
        
        notas = [n.calificacion for n in self.sistema.notas_heap]
        if notas:
            # Colores más atractivos
            colors = ['#ff6b6b', '#feca57', '#48dbfb', '#0abde3', '#00d2d3']
            n, bins, patches = ax1.hist(notas, bins=10, edgecolor='white', linewidth=1.5)
            
            # Aplicar colores
            for i, patch in enumerate(patches):
                patch.set_facecolor(colors[i % len(colors)])
                patch.set_alpha(0.8)
            
            ax1.set_title('Distribución de Notas', fontweight='bold', color='#2c3e50', fontsize=12)
            ax1.set_xlabel('Calificación', fontweight='bold', color='#2c3e50', fontsize=10)
            ax1.set_ylabel('Cantidad', fontweight='bold', color='#2c3e50', fontsize=10)
            ax1.set_xticks([0, 1, 2, 3, 4, 5])
            ax1.grid(True, linestyle='--', alpha=0.5, color='#bdc3c7')
            ax1.set_facecolor('#f8f9fa')
            
            # Mejorar bordes
            for spine in ax1.spines.values():
                spine.set_edgecolor('#bdc3c7')
                spine.set_linewidth(1)
        
        # Gráfico 2: Estudiantes en riesgo vs aprobados mejorado
        self.figure2.clear()
        ax2 = self.figure2.add_subplot(111)
        
        estudiantes = [e.codigo for e in self.sistema.obtener_estudiantes()]
        aprobados = 0
        riesgo = 0
        
        for codigo in estudiantes:
            prom = self.sistema.calcular_promedio_estudiante(codigo)
            if prom < 3.0:
                riesgo += 1
            else:
                aprobados += 1
        
        if estudiantes:
            labels = ['Aprobados', 'En Riesgo']
            sizes = [aprobados, riesgo]
            colors = ['#2ecc71', '#e74c3c']
            explode = (0.05, 0.1)
            
            wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   startangle=90, shadow=True, explode=explode, 
                   textprops={'fontweight': 'bold', 'color': '#2c3e50', 'fontsize': 9})
            
            # Mejorar el texto de porcentajes
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            ax2.set_title('Aprobados vs En Riesgo', fontweight='bold', color='#2c3e50', fontsize=12)
            ax2.set_facecolor('#f8f9fa')
        
        # Ajustar layout con márgenes más pequeños
        self.figure1.tight_layout(pad=1.5)
        self.figure2.tight_layout(pad=1.5)
        
        self.canvas1.draw()
        self.canvas2.draw()