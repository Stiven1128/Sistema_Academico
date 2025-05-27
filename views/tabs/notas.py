from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                            QLabel, QFrame, QLineEdit, QComboBox, QGroupBox, QGridLayout,
                            QSplitter, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPalette
from models.estudiante import Estudiante
from models.asignatura import Asignatura
from models.nota import Nota
from models.sistema_notas import SistemaNotas

class NotesTab(QWidget):
    """Pestaña de gestión de notas con diseño moderno"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.setup_modern_ui()
        self.apply_modern_styles()
    
    def setup_modern_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header con título y estadísticas
        self.create_header_section(main_layout)
        
        # Sección de filtros y búsqueda
        self.create_filter_section(main_layout)
        
        # Sección principal con tabla y estadísticas
        self.create_main_content_section(main_layout)
        
        # Sección de acciones
        self.create_action_section(main_layout)
        
        self.setLayout(main_layout)
        
        # Actualizar tabla y estadísticas
        self.update_table()
        self.update_statistics()
    
    def create_header_section(self, parent_layout):
        """Crear sección de encabezado con título y estadísticas"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        
        # Título principal
        title_layout = QHBoxLayout()
        
        title_label = QLabel("📝 Gestión de Calificaciones")
        title_label.setObjectName("titleLabel")
        
        # Contador de notas
        self.notes_count_label = QLabel("0 calificaciones registradas")
        self.notes_count_label.setObjectName("countLabel")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.notes_count_label)
        
        # Estadísticas rápidas
        stats_layout = QHBoxLayout()
        
        self.avg_grade_label = QLabel("📊 Promedio General: --")
        self.avg_grade_label.setObjectName("statLabel")
        
        self.highest_grade_label = QLabel("🏆 Nota Más Alta: --")
        self.highest_grade_label.setObjectName("statLabel")
        
        self.lowest_grade_label = QLabel("📉 Nota Más Baja: --")
        self.lowest_grade_label.setObjectName("statLabel")
        
        stats_layout.addWidget(self.avg_grade_label)
        stats_layout.addWidget(self.highest_grade_label)
        stats_layout.addWidget(self.lowest_grade_label)
        stats_layout.addStretch()
        
        header_layout.addLayout(title_layout)
        header_layout.addLayout(stats_layout)
        
        parent_layout.addWidget(header_frame)
    
    def create_filter_section(self, parent_layout):
        """Crear sección de filtros y búsqueda"""
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(20, 15, 20, 15)
        
        # Búsqueda por texto
        search_label = QLabel("🔍 Buscar:")
        search_label.setObjectName("filterLabel")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por estudiante, asignatura o descripción...")
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_table)
        
        # Filtro por estudiante
        student_label = QLabel("👤 Estudiante:")
        student_label.setObjectName("filterLabel")
        
        self.student_filter = QComboBox()
        self.student_filter.setObjectName("filterCombo")
        self.student_filter.currentTextChanged.connect(self.filter_table)
        
        # Filtro por asignatura
        subject_label = QLabel("📚 Asignatura:")
        subject_label.setObjectName("filterLabel")
        
        self.subject_filter = QComboBox()
        self.subject_filter.setObjectName("filterCombo")
        self.subject_filter.currentTextChanged.connect(self.filter_table)
        
        # Filtro por rango de calificación
        grade_label = QLabel("📊 Calificación:")
        grade_label.setObjectName("filterLabel")
        
        self.grade_filter = QComboBox()
        self.grade_filter.setObjectName("filterCombo")
        self.grade_filter.addItems(["Todas", "Excelente (4.5-5.0)", "Buena (4.0-4.4)", 
                                   "Aceptable (3.0-3.9)", "Deficiente (<3.0)"])
        self.grade_filter.currentTextChanged.connect(self.filter_table)
        
        # Botón limpiar filtros
        clear_filters_btn = QPushButton("🗑️ Limpiar")
        clear_filters_btn.setObjectName("clearButton")
        clear_filters_btn.clicked.connect(self.clear_filters)
        
        # Organizar elementos
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(student_label)
        filter_layout.addWidget(self.student_filter, 1)
        filter_layout.addWidget(subject_label)
        filter_layout.addWidget(self.subject_filter, 1)
        filter_layout.addWidget(grade_label)
        filter_layout.addWidget(self.grade_filter, 1)
        filter_layout.addWidget(clear_filters_btn)
        
        parent_layout.addWidget(filter_frame)
    
    def create_main_content_section(self, parent_layout):
        """Crear sección principal con tabla y panel de información"""
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Tabla de notas
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de la tabla
        table_title = QLabel("📋 Lista de Calificaciones")
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Tabla de notas mejorada
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "👤 Estudiante", "📚 Asignatura", "📊 Calificación", 
            "📅 Fecha", "⚖️ Peso", "📝 Descripción", "🎯 Estado"
        ])
        
        # Configurar tabla
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Estudiante
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Asignatura
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)  # Descripción
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setObjectName("notesTable")
        
        # Conectar doble clic para editar
        self.table.doubleClicked.connect(self.edit_note)
        
        table_layout.addWidget(self.table)
        
        # Panel derecho - Información y estadísticas
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setFixedWidth(300)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        # Información de la nota seleccionada
        self.create_note_info_panel(info_layout)
        
        # Estadísticas por asignatura
        self.create_subject_stats_panel(info_layout)
        
        # Agregar al splitter
        content_splitter.addWidget(table_frame)
        content_splitter.addWidget(info_frame)
        content_splitter.setSizes([800, 300])
        
        parent_layout.addWidget(content_splitter)
    
    def create_note_info_panel(self, parent_layout):
        """Crear panel de información de nota seleccionada"""
        info_group = QGroupBox("ℹ️ Información de Calificación")
        info_group.setObjectName("infoGroup")
        info_layout = QVBoxLayout(info_group)
        
        self.selected_note_info = QLabel("Seleccione una calificación para ver detalles")
        self.selected_note_info.setObjectName("noteInfo")
        self.selected_note_info.setWordWrap(True)
        
        info_layout.addWidget(self.selected_note_info)
        
        # Conectar selección de tabla
        self.table.itemSelectionChanged.connect(self.update_selected_note_info)
        
        parent_layout.addWidget(info_group)
    
    def create_subject_stats_panel(self, parent_layout):
        """Crear panel de estadísticas por asignatura"""
        stats_group = QGroupBox("📈 Estadísticas Rápidas")
        stats_group.setObjectName("statsGroup")
        stats_layout = QVBoxLayout(stats_group)
        
        self.quick_stats_label = QLabel("Estadísticas del sistema")
        self.quick_stats_label.setObjectName("quickStats")
        self.quick_stats_label.setWordWrap(True)
        
        stats_layout.addWidget(self.quick_stats_label)
        
        parent_layout.addWidget(stats_group)
        parent_layout.addStretch()
    
    def create_action_section(self, parent_layout):
        """Crear sección de botones de acción"""
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botones principales
        self.add_note_btn = QPushButton("➕ Nueva Calificación")
        self.add_note_btn.setObjectName("primaryButton")
        self.add_note_btn.clicked.connect(self.parent.show_add_note_dialog)
        
        self.edit_note_btn = QPushButton("✏️ Editar")
        self.edit_note_btn.setObjectName("secondaryButton")
        self.edit_note_btn.clicked.connect(self.edit_note)
        
        self.delete_note_btn = QPushButton("🗑️ Eliminar")
        self.delete_note_btn.setObjectName("dangerButton")
        self.delete_note_btn.clicked.connect(self.delete_note)
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setObjectName("secondaryButton")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("🏠 Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.parent.show_dashboard)
        
        # Organizar botones
        action_layout.addWidget(self.add_note_btn)
        action_layout.addWidget(self.edit_note_btn)
        action_layout.addWidget(self.delete_note_btn)
        action_layout.addStretch()
        action_layout.addWidget(self.refresh_btn)
        action_layout.addWidget(back_btn)
        
        parent_layout.addWidget(action_frame)
    
    def apply_modern_styles(self):
        """Aplicar estilos modernos a la pestaña"""
        self.setStyleSheet("""
            /* Frame principal */
            QWidget {
                background-color: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Header */
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                color: white;
            }
            
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
            }
            
            #countLabel {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 500;
            }
            
            #statLabel {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.95);
                font-weight: 500;
                padding: 5px 10px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                margin: 2px;
            }
            
            /* Filtros */
            #filterFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
            }
            
            #filterLabel {
                font-weight: bold;
                color: #495057;
                font-size: 13px;
            }
            
            #searchInput {
                padding: 8px 12px;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                font-size: 13px;
                background-color: #f8f9fa;
            }
            
            #searchInput:focus {
                border-color: #667eea;
                background-color: white;
            }
            
            #filterCombo {
                padding: 6px 10px;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                min-width: 120px;
            }
            
            #filterCombo:focus {
                border-color: #667eea;
            }
            
            #clearButton {
                padding: 8px 15px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            
            #clearButton:hover {
                background-color: #5a6268;
            }
            
            /* Tabla */
            #tableFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
            }
            
            #sectionTitle {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            #notesTable {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #e9ecef;
            }
            
            #notesTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            
            #notesTable::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            #notesTable::item:hover {
                background-color: #f8f9fa;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #495057;
                padding: 10px;
                border: 1px solid #dee2e6;
                font-weight: bold;
                font-size: 12px;
            }
            
            /* Panel de información */
            #infoFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
            }
            
            #infoGroup, #statsGroup {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            
            #noteInfo, #quickStats {
                color: #495057;
                font-size: 13px;
                line-height: 1.4;
                padding: 10px;
            }
            
            /* Botones de acción */
            #actionFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
            }
            
            #primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            
            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1e7e34);
            }
            
            #secondaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #secondaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
            
            #dangerButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #dangerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
            
            #backButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #backButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #343a40);
            }
        """)
    
    def update_table(self):
        """Actualizar tabla con todas las notas"""
        self.table.setRowCount(0)
        
        # Actualizar filtros
        self.update_filter_combos()
        
        # Ordenar notas por estudiante y asignatura
        notas_ordenadas = sorted(self.sistema.notas_heap, key=lambda x: (
            self.sistema.estudiantes.get(x.estudiante, Estudiante("", x.estudiante, "")).nombre,
            self.sistema.asignaturas.get(x.asignatura, Asignatura("", x.asignatura)).nombre
        ))
        
        for nota in notas_ordenadas:
            self.add_note_to_table(nota)
        
        # Actualizar contador
        self.notes_count_label.setText(f"{len(notas_ordenadas)} calificaciones registradas")
    
    def add_note_to_table(self, nota):
        """Agregar una nota a la tabla"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Obtener nombres de estudiante y asignatura
        estudiante = self.sistema.estudiantes.get(nota.estudiante, None)
        nombre_estudiante = estudiante.nombre if estudiante else nota.estudiante
        
        asignatura = self.sistema.asignaturas.get(nota.asignatura, None)
        nombre_asignatura = asignatura.nombre if asignatura else nota.asignatura
        
        # Determinar estado de la calificación
        if nota.calificacion >= 4.5:
            estado = "🌟 Excelente"
            color_estado = QColor(46, 204, 113)
        elif nota.calificacion >= 4.0:
            estado = "✅ Buena"
            color_estado = QColor(52, 152, 219)
        elif nota.calificacion >= 3.0:
            estado = "⚠️ Aceptable"
            color_estado = QColor(241, 196, 15)
        else:
            estado = "❌ Deficiente"
            color_estado = QColor(231, 76, 60)
        
        # Crear items para la tabla
        items = [
            QTableWidgetItem(nombre_estudiante),
            QTableWidgetItem(nombre_asignatura),
            QTableWidgetItem(f"{nota.calificacion:.2f}"),
            QTableWidgetItem(nota.fecha.strftime('%d/%m/%Y')),
            QTableWidgetItem(f"{nota.peso:.1f}%"),
            QTableWidgetItem(nota.descripcion),
            QTableWidgetItem(estado)
        ]
        
        # Aplicar colores según la calificación
        items[2].setForeground(QBrush(color_estado))
        items[2].setFont(QFont("Arial", 10, QFont.Bold))
        
        items[6].setForeground(QBrush(color_estado))
        items[6].setFont(QFont("Arial", 9, QFont.Bold))
        
        # Hacer celdas no editables
        for col, item in enumerate(items):
            self.table.setItem(row, col, item)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def update_filter_combos(self):
        """Actualizar los combos de filtro"""
        # Guardar selecciones actuales
        current_student = self.student_filter.currentText()
        current_subject = self.subject_filter.currentText()
        
        # Limpiar combos
        self.student_filter.clear()
        self.subject_filter.clear()
        
        # Agregar opción "Todos"
        self.student_filter.addItem("Todos los estudiantes")
        self.subject_filter.addItem("Todas las asignaturas")
        
        # Agregar estudiantes
        for estudiante in self.sistema.estudiantes.values():
            self.student_filter.addItem(estudiante.nombre)
        
        # Agregar asignaturas
        for asignatura in self.sistema.asignaturas.values():
            self.subject_filter.addItem(asignatura.nombre)
        
        # Restaurar selecciones si existen
        student_index = self.student_filter.findText(current_student)
        if student_index >= 0:
            self.student_filter.setCurrentIndex(student_index)
        
        subject_index = self.subject_filter.findText(current_subject)
        if subject_index >= 0:
            self.subject_filter.setCurrentIndex(subject_index)
    
    def filter_table(self):
        """Filtrar tabla según criterios seleccionados"""
        search_text = self.search_input.text().lower()
        selected_student = self.student_filter.currentText()
        selected_subject = self.subject_filter.currentText()
        selected_grade = self.grade_filter.currentText()
        
        for row in range(self.table.rowCount()):
            show_row = True
            
            # Filtro por texto de búsqueda
            if search_text:
                row_text = ""
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        row_text += item.text().lower() + " "
                
                if search_text not in row_text:
                    show_row = False
            
            # Filtro por estudiante
            if selected_student != "Todos los estudiantes":
                student_item = self.table.item(row, 0)
                if student_item and student_item.text() != selected_student:
                    show_row = False
            
            # Filtro por asignatura
            if selected_subject != "Todas las asignaturas":
                subject_item = self.table.item(row, 1)
                if subject_item and subject_item.text() != selected_subject:
                    show_row = False
            
            # Filtro por calificación
            if selected_grade != "Todas":
                grade_item = self.table.item(row, 2)
                if grade_item:
                    try:
                        grade = float(grade_item.text())
                        if selected_grade == "Excelente (4.5-5.0)" and not (4.5 <= grade <= 5.0):
                            show_row = False
                        elif selected_grade == "Buena (4.0-4.4)" and not (4.0 <= grade < 4.5):
                            show_row = False
                        elif selected_grade == "Aceptable (3.0-3.9)" and not (3.0 <= grade < 4.0):
                            show_row = False
                        elif selected_grade == "Deficiente (<3.0)" and not (grade < 3.0):
                            show_row = False
                    except ValueError:
                        show_row = False
            
            self.table.setRowHidden(row, not show_row)
    
    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.search_input.clear()
        self.student_filter.setCurrentIndex(0)
        self.subject_filter.setCurrentIndex(0)
        self.grade_filter.setCurrentIndex(0)
    
    def update_statistics(self):
        """Actualizar estadísticas generales"""
        if not self.sistema.notas_heap:
            self.avg_grade_label.setText("📊 Promedio General: --")
            self.highest_grade_label.setText("🏆 Nota Más Alta: --")
            self.lowest_grade_label.setText("📉 Nota Más Baja: --")
            return
        
        # Calcular estadísticas
        calificaciones = [nota.calificacion for nota in self.sistema.notas_heap]
        promedio = sum(calificaciones) / len(calificaciones)
        nota_alta = max(calificaciones)
        nota_baja = min(calificaciones)
        
        # Actualizar labels
        self.avg_grade_label.setText(f"📊 Promedio General: {promedio:.2f}")
        self.highest_grade_label.setText(f"🏆 Nota Más Alta: {nota_alta:.2f}")
        self.lowest_grade_label.setText(f"📉 Nota Más Baja: {nota_baja:.2f}")
        
        # Actualizar estadísticas rápidas
        total_excelentes = len([n for n in calificaciones if n >= 4.5])
        total_deficientes = len([n for n in calificaciones if n < 3.0])
        
        stats_text = f"""
        📈 Total de calificaciones: {len(calificaciones)}
        🌟 Excelentes (≥4.5): {total_excelentes}
        ❌ Deficientes (<3.0): {total_deficientes}
        📊 Promedio: {promedio:.2f}
        
        🎯 Distribución:
        • Excelente: {(total_excelentes/len(calificaciones)*100):.1f}%
        • Deficiente: {(total_deficientes/len(calificaciones)*100):.1f}%
        """
        
        self.quick_stats_label.setText(stats_text.strip())
    
    def update_selected_note_info(self):
        """Actualizar información de la nota seleccionada"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            self.selected_note_info.setText("Seleccione una calificación para ver detalles")
            return
        
        # Obtener información de la fila seleccionada
        estudiante = self.table.item(selected_row, 0).text()
        asignatura = self.table.item(selected_row, 1).text()
        calificacion = self.table.item(selected_row, 2).text()
        fecha = self.table.item(selected_row, 3).text()
        peso = self.table.item(selected_row, 4).text()
        descripcion = self.table.item(selected_row, 5).text()
        estado = self.table.item(selected_row, 6).text()
        
        info_text = f"""
        👤 <b>Estudiante:</b> {estudiante}
        📚 <b>Asignatura:</b> {asignatura}
        📊 <b>Calificación:</b> {calificacion}
        📅 <b>Fecha:</b> {fecha}
        ⚖️ <b>Peso:</b> {peso}
        🎯 <b>Estado:</b> {estado}
        
        📝 <b>Descripción:</b>
        {descripcion}
        """
        
        self.selected_note_info.setText(info_text.strip())
    
    def refresh_data(self):
        """Actualizar todos los datos"""
        self.update_table()
        self.update_statistics()
        
        # Mostrar mensaje de confirmación
        self.parent.statusBar().showMessage("🔄 Datos actualizados correctamente", 2000)
    
    def edit_note(self):
        """Editar nota seleccionada"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione una calificación para editar.")
            return
        
        # Obtener índice real considerando filtros
        visible_rows = []
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                visible_rows.append(row)
        
        if selected >= len(visible_rows):
            return
        
        actual_index = visible_rows[selected]
        if actual_index < len(self.sistema.notas_heap):
            nota = self.sistema.notas_heap[actual_index]
            self.parent.show_edit_note_dialog(nota)
    
    def delete_note(self):
        """Eliminar nota seleccionada"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione una calificación para eliminar.")
            return
        
        # Obtener información de la nota
        estudiante = self.table.item(selected, 0).text()
        asignatura = self.table.item(selected, 1).text()
        calificacion = self.table.item(selected, 2).text()
        
        reply = QMessageBox.question(
            self, "🗑️ Confirmar Eliminación", 
            f"¿Está seguro que desea eliminar esta calificación?\n\n"
            f"👤 Estudiante: {estudiante}\n"
            f"📚 Asignatura: {asignatura}\n"
            f"📊 Calificación: {calificacion}\n\n"
            f"Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Obtener índice real considerando filtros
            visible_rows = []
            for row in range(self.table.rowCount()):
                if not self.table.isRowHidden(row):
                    visible_rows.append(row)
            
            if selected >= len(visible_rows):
                return
            
            actual_index = visible_rows[selected]
            if self.sistema.eliminar_nota(actual_index):
                QMessageBox.information(self, "✅ Éxito", 
                                      "Calificación eliminada correctamente.")
                self.refresh_data()
                self.parent.dashboard.update_stats()
                self.parent.update_system_info()
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  "No se pudo eliminar la calificación.")