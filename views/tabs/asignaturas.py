from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                            QLabel, QFrame, QLineEdit, QComboBox, QGroupBox, QGridLayout,
                            QSplitter, QScrollArea, QProgressBar, QSpinBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPalette

class SubjectsTab(QWidget):
    """Pestaña de gestión de asignaturas con diseño moderno"""
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
        
        # Sección principal con tabla y panel de información
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
        
        title_label = QLabel("📚 Gestión de Asignaturas")
        title_label.setObjectName("titleLabel")
        
        # Contador de asignaturas
        self.subjects_count_label = QLabel("0 asignaturas registradas")
        self.subjects_count_label.setObjectName("countLabel")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.subjects_count_label)
        
        # Estadísticas rápidas
        stats_layout = QHBoxLayout()
        
        self.total_credits_label = QLabel("🎓 Total Créditos: --")
        self.total_credits_label.setObjectName("statLabel")
        
        self.avg_credits_label = QLabel("📊 Promedio Créditos: --")
        self.avg_credits_label.setObjectName("statLabel")
        
        self.professors_count_label = QLabel("👨‍🏫 Profesores Asignados: --")
        self.professors_count_label.setObjectName("statLabel")
        
        self.subjects_with_grades_label = QLabel("📝 Con Calificaciones: --")
        self.subjects_with_grades_label.setObjectName("statLabel")
        
        stats_layout.addWidget(self.total_credits_label)
        stats_layout.addWidget(self.avg_credits_label)
        stats_layout.addWidget(self.professors_count_label)
        stats_layout.addWidget(self.subjects_with_grades_label)
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
        self.search_input.setPlaceholderText("Buscar por código, nombre o profesor...")
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_table)
        
        # Filtro por profesor
        professor_label = QLabel("👨‍🏫 Profesor:")
        professor_label.setObjectName("filterLabel")
        
        self.professor_filter = QComboBox()
        self.professor_filter.setObjectName("filterCombo")
        self.professor_filter.currentTextChanged.connect(self.filter_table)
        
        # Filtro por rango de créditos
        credits_label = QLabel("🎓 Créditos:")
        credits_label.setObjectName("filterLabel")
        
        self.credits_filter = QComboBox()
        self.credits_filter.setObjectName("filterCombo")
        self.credits_filter.addItems(["Todos", "1-2 créditos", "3-4 créditos", "5+ créditos"])
        self.credits_filter.currentTextChanged.connect(self.filter_table)
        
        # Filtro por estado
        status_label = QLabel("📊 Estado:")
        status_label.setObjectName("filterLabel")
        
        self.status_filter = QComboBox()
        self.status_filter.setObjectName("filterCombo")
        self.status_filter.addItems(["Todas", "Con Calificaciones", "Sin Calificaciones", "Sin Profesor"])
        self.status_filter.currentTextChanged.connect(self.filter_table)
        
        # Botón limpiar filtros
        clear_filters_btn = QPushButton("🗑️ Limpiar")
        clear_filters_btn.setObjectName("clearButton")
        clear_filters_btn.clicked.connect(self.clear_filters)
        
        # Organizar elementos
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(professor_label)
        filter_layout.addWidget(self.professor_filter, 1)
        filter_layout.addWidget(credits_label)
        filter_layout.addWidget(self.credits_filter, 1)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter, 1)
        filter_layout.addWidget(clear_filters_btn)
        
        parent_layout.addWidget(filter_frame)

    def create_main_content_section(self, parent_layout):
        """Crear sección principal con tabla y panel de información"""
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Tabla de asignaturas
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de la tabla
        table_title = QLabel("📋 Lista de Asignaturas")
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Tabla de asignaturas mejorada
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "🔢 Código", "📚 Nombre", "🎓 Créditos", 
            "👨‍🏫 Profesor", "📊 Promedio", "🎯 Estado"
        ])
        
        # Configurar tabla
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Nombre
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)  # Profesor
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setObjectName("subjectsTable")
        
        # Conectar doble clic para editar
        self.table.doubleClicked.connect(self.edit_subject)
        
        table_layout.addWidget(self.table)
        
        # Panel derecho - Información de la asignatura
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setFixedWidth(350)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        # Información de la asignatura seleccionada
        self.create_subject_info_panel(info_layout)
        
        # Estadísticas de la asignatura
        self.create_subject_stats_panel(info_layout)
        
        # Agregar al splitter
        content_splitter.addWidget(table_frame)
        content_splitter.addWidget(info_frame)
        content_splitter.setSizes([750, 350])
        
        parent_layout.addWidget(content_splitter)

    def create_subject_info_panel(self, parent_layout):
        """Crear panel de información de asignatura seleccionada"""
        info_group = QGroupBox("📚 Información de la Asignatura")
        info_group.setObjectName("infoGroup")
        info_layout = QVBoxLayout(info_group)
        
        self.selected_subject_info = QLabel("Seleccione una asignatura para ver detalles")
        self.selected_subject_info.setObjectName("subjectInfo")
        self.selected_subject_info.setWordWrap(True)
        
        info_layout.addWidget(self.selected_subject_info)
        
        # Conectar selección de tabla
        self.table.itemSelectionChanged.connect(self.update_selected_subject_info)
        
        parent_layout.addWidget(info_group)

    def create_subject_stats_panel(self, parent_layout):
        """Crear panel de estadísticas de la asignatura"""
        stats_group = QGroupBox("📊 Estadísticas de Rendimiento")
        stats_group.setObjectName("statsGroup")
        stats_layout = QVBoxLayout(stats_group)
        
        # Promedio de la asignatura
        self.subject_avg_label = QLabel("📊 Promedio: --")
        self.subject_avg_label.setObjectName("statText")
        
        # Barra de progreso visual
        self.subject_progress_bar = QProgressBar()
        self.subject_progress_bar.setRange(0, 50)  # 0 a 5.0 * 10
        self.subject_progress_bar.setValue(0)
        self.subject_progress_bar.setObjectName("progressBar")
        
        # Estado de la asignatura
        self.subject_status_label = QLabel("🎯 Estado: --")
        self.subject_status_label.setObjectName("statusLabel")
        
        # Estadísticas detalladas
        self.subject_details_label = QLabel("📈 Estadísticas: --")
        self.subject_details_label.setObjectName("detailsText")
        self.subject_details_label.setWordWrap(True)
        
        # Información del profesor
        professor_info_group = QGroupBox("👨‍🏫 Información del Profesor")
        professor_info_group.setObjectName("professorGroup")
        professor_info_layout = QVBoxLayout(professor_info_group)
        
        self.professor_info_label = QLabel("Sin profesor asignado")
        self.professor_info_label.setObjectName("professorInfo")
        self.professor_info_label.setWordWrap(True)
        
        professor_info_layout.addWidget(self.professor_info_label)
        
        stats_layout.addWidget(self.subject_avg_label)
        stats_layout.addWidget(self.subject_progress_bar)
        stats_layout.addWidget(self.subject_status_label)
        stats_layout.addWidget(self.subject_details_label)
        
        parent_layout.addWidget(stats_group)
        parent_layout.addWidget(professor_info_group)
        parent_layout.addStretch()

    def create_action_section(self, parent_layout):
        """Crear sección de botones de acción"""
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botones principales
        self.add_subject_btn = QPushButton("➕ Nueva Asignatura")
        self.add_subject_btn.setObjectName("primaryButton")
        self.add_subject_btn.clicked.connect(self.parent.show_add_subject_dialog)
        
        self.edit_subject_btn = QPushButton("✏️ Editar")
        self.edit_subject_btn.setObjectName("secondaryButton")
        self.edit_subject_btn.clicked.connect(self.edit_subject)
        
        self.delete_subject_btn = QPushButton("🗑️ Eliminar")
        self.delete_subject_btn.setObjectName("dangerButton")
        self.delete_subject_btn.clicked.connect(self.delete_subject)
        
        self.view_grades_btn = QPushButton("📊 Ver Calificaciones")
        self.view_grades_btn.setObjectName("infoButton")
        self.view_grades_btn.clicked.connect(self.view_subject_grades)
        
        self.assign_professor_btn = QPushButton("👨‍🏫 Asignar Profesor")
        self.assign_professor_btn.setObjectName("specialButton")
        self.assign_professor_btn.clicked.connect(self.assign_professor)
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setObjectName("secondaryButton")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("🏠 Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.parent.show_dashboard)
        
        # Organizar botones
        action_layout.addWidget(self.add_subject_btn)
        action_layout.addWidget(self.edit_subject_btn)
        action_layout.addWidget(self.delete_subject_btn)
        action_layout.addWidget(self.view_grades_btn)
        action_layout.addWidget(self.assign_professor_btn)
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
            
            #subjectsTable {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #e9ecef;
            }
            
            #subjectsTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            
            #subjectsTable::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            #subjectsTable::item:hover {
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
            
            #infoGroup, #statsGroup, #professorGroup {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            
            #subjectInfo, #professorInfo, #detailsText {
                color: #495057;
                font-size: 13px;
                line-height: 1.4;
                padding: 10px;
            }
            
            #statText, #statusLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                margin: 5px 0;
            }
            
            #progressBar {
                height: 20px;
                border-radius: 10px;
                background-color: #e9ecef;
                margin: 5px 0;
            }
            
            #progressBar::chunk {
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28a745, stop:0.5 #ffc107, stop:1 #dc3545);
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
            
            #infoButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #infoButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #117a8b);
            }
            
            #specialButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fd7e14, stop:1 #e55a4e);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #specialButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e55a4e, stop:1 #dc3545);
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
        """Actualizar tabla con todas las asignaturas"""
        self.table.setRowCount(0)
        
        # Actualizar filtros
        self.update_filter_combos()
        
        # Obtener asignaturas ordenadas
        asignaturas = sorted(self.sistema.obtener_asignaturas(), key=lambda x: x.nombre)
        
        for asignatura in asignaturas:
            self.add_subject_to_table(asignatura)
        
        # Actualizar contador
        self.subjects_count_label.setText(f"{len(asignaturas)} asignaturas registradas")

    def add_subject_to_table(self, asignatura):
        """Agregar una asignatura a la tabla"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Obtener nombre del profesor
        profesor = self.sistema.profesores.get(asignatura.profesor, None)
        nombre_profesor = profesor.nombre if profesor else "Sin asignar"
        
        # Calcular promedio de la asignatura
        promedio = self.sistema.calcular_promedio_asignatura(asignatura.codigo)
        promedio_str = f"{promedio:.2f}" if promedio > 0 else "Sin notas"
        
        # Determinar estado de la asignatura
        notas_asignatura = [n for n in self.sistema.notas_heap if n.asignatura == asignatura.codigo]
        
        if not notas_asignatura:
            estado = "📝 Sin calificaciones"
            color_estado = QColor(108, 117, 125)  # Gris
        elif not profesor:
            estado = "⚠️ Sin profesor"
            color_estado = QColor(255, 193, 7)  # Amarillo
        elif promedio >= 4.0:
            estado = "🌟 Excelente"
            color_estado = QColor(46, 204, 113)  # Verde
        elif promedio >= 3.0:
            estado = "✅ Buena"
            color_estado = QColor(52, 152, 219)  # Azul
        else:
            estado = "❌ Necesita atención"
            color_estado = QColor(231, 76, 60)  # Rojo
        
        # Determinar color de créditos
        if asignatura.creditos >= 5:
            creditos_color = QColor(46, 204, 113)  # Verde para muchos créditos
        elif asignatura.creditos >= 3:
            creditos_color = QColor(52, 152, 219)  # Azul para créditos normales
        else:
            creditos_color = QColor(241, 196, 15)  # Amarillo para pocos créditos
        
        # Crear items para la tabla
        items = [
            QTableWidgetItem(asignatura.codigo),
            QTableWidgetItem(asignatura.nombre),
            QTableWidgetItem(str(asignatura.creditos)),
            QTableWidgetItem(nombre_profesor),
            QTableWidgetItem(promedio_str),
            QTableWidgetItem(estado)
        ]
        
        # Aplicar colores y formato
        items[2].setForeground(QBrush(creditos_color))
        items[2].setFont(QFont("Arial", 10, QFont.Bold))
        
        if promedio > 0:
            promedio_color = QColor(46, 204, 113) if promedio >= 4.0 else QColor(231, 76, 60) if promedio < 3.0 else QColor(241, 196, 15)
            items[4].setForeground(QBrush(promedio_color))
            items[4].setFont(QFont("Arial", 10, QFont.Bold))
        else:
            items[4].setForeground(QBrush(QColor(108, 117, 125)))
        
        items[5].setForeground(QBrush(color_estado))
        items[5].setFont(QFont("Arial", 9, QFont.Bold))
        
        # Hacer celdas no editables
        for col, item in enumerate(items):
            self.table.setItem(row, col, item)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)

    def update_filter_combos(self):
        """Actualizar los combos de filtro"""
        # Guardar selecciones actuales
        current_professor = self.professor_filter.currentText()
        
        # Limpiar combo de profesores
        self.professor_filter.clear()
        
        # Agregar opción "Todos"
        self.professor_filter.addItem("Todos los profesores")
        
        # Agregar profesores únicos
        profesores_asignados = set()
        for asignatura in self.sistema.asignaturas.values():
            if asignatura.profesor:
                profesor = self.sistema.profesores.get(asignatura.profesor)
                if profesor:
                    profesores_asignados.add(profesor.nombre)
        
        # Agregar profesores ordenados
        for profesor_nombre in sorted(profesores_asignados):
            self.professor_filter.addItem(profesor_nombre)
        
        # Agregar opción para asignaturas sin profesor
        self.professor_filter.addItem("Sin profesor asignado")
        
        # Restaurar selección si existe
        professor_index = self.professor_filter.findText(current_professor)
        if professor_index >= 0:
            self.professor_filter.setCurrentIndex(professor_index)

    def filter_table(self):
        """Filtrar tabla según criterios seleccionados"""
        search_text = self.search_input.text().lower()
        selected_professor = self.professor_filter.currentText()
        selected_credits = self.credits_filter.currentText()
        selected_status = self.status_filter.currentText()
        
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
            
            # Filtro por profesor
            if selected_professor != "Todos los profesores":
                professor_item = self.table.item(row, 3)
                if professor_item:
                    if selected_professor == "Sin profesor asignado":
                        if professor_item.text() != "Sin asignar":
                            show_row = False
                    else:
                        if professor_item.text() != selected_professor:
                            show_row = False
            
            # Filtro por créditos
            if selected_credits != "Todos":
                credits_item = self.table.item(row, 2)
                if credits_item:
                    try:
                        credits = int(credits_item.text())
                        if selected_credits == "1-2 créditos" and not (1 <= credits <= 2):
                            show_row = False
                        elif selected_credits == "3-4 créditos" and not (3 <= credits <= 4):
                            show_row = False
                        elif selected_credits == "5+ créditos" and credits < 5:
                            show_row = False
                    except ValueError:
                        show_row = False
            
            # Filtro por estado
            if selected_status != "Todas":
                status_item = self.table.item(row, 5)
                promedio_item = self.table.item(row, 4)
                professor_item = self.table.item(row, 3)
                
                if status_item and promedio_item and professor_item:
                    has_grades = promedio_item.text() != "Sin notas"
                    has_professor = professor_item.text() != "Sin asignar"
                    
                    if selected_status == "Con Calificaciones" and not has_grades:
                        show_row = False
                    elif selected_status == "Sin Calificaciones" and has_grades:
                        show_row = False
                    elif selected_status == "Sin Profesor" and has_professor:
                        show_row = False
            
            self.table.setRowHidden(row, not show_row)

    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.search_input.clear()
        self.professor_filter.setCurrentIndex(0)
        self.credits_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)

    def update_statistics(self):
        """Actualizar estadísticas generales"""
        asignaturas = list(self.sistema.asignaturas.values())
        
        if not asignaturas:
            self.total_credits_label.setText("🎓 Total Créditos: --")
            self.avg_credits_label.setText("📊 Promedio Créditos: --")
            self.professors_count_label.setText("👨‍🏫 Profesores Asignados: --")
            self.subjects_with_grades_label.setText("📝 Con Calificaciones: --")
            return
        
        # Calcular estadísticas
        total_creditos = sum(a.creditos for a in asignaturas)
        promedio_creditos = total_creditos / len(asignaturas)
        
        # Contar profesores únicos asignados
        profesores_asignados = set()
        for asignatura in asignaturas:
            if asignatura.profesor:
                profesores_asignados.add(asignatura.profesor)
        
        # Contar asignaturas con calificaciones
        asignaturas_con_notas = 0
        for asignatura in asignaturas:
            notas = [n for n in self.sistema.notas_heap if n.asignatura == asignatura.codigo]
            if notas:
                asignaturas_con_notas += 1
        
        # Actualizar labels
        self.total_credits_label.setText(f"🎓 Total Créditos: {total_creditos}")
        self.avg_credits_label.setText(f"📊 Promedio Créditos: {promedio_creditos:.1f}")
        self.professors_count_label.setText(f"👨‍🏫 Profesores Asignados: {len(profesores_asignados)}")
        self.subjects_with_grades_label.setText(f"📝 Con Calificaciones: {asignaturas_con_notas}")

    def update_selected_subject_info(self):
        """Actualizar información de la asignatura seleccionada"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            self.selected_subject_info.setText("Seleccione una asignatura para ver detalles")
            self.clear_subject_stats()
            return
        
        # Obtener información de la asignatura
        codigo = self.table.item(selected_row, 0).text()
        asignatura = self.sistema.asignaturas.get(codigo)
        
        if not asignatura:
            self.clear_subject_stats()
            return
        
        # Información básica
        info_text = f"""
        🔢 <b>Código:</b> {asignatura.codigo}
        📚 <b>Nombre:</b> {asignatura.nombre}
        🎓 <b>Créditos:</b> {asignatura.creditos}
        """
        self.selected_subject_info.setText(info_text.strip())
        
        # Información del profesor
        if asignatura.profesor:
            profesor = self.sistema.profesores.get(asignatura.profesor)
            if profesor:
                profesor_text = f"""
                👨‍🏫 <b>Nombre:</b> {profesor.nombre}
                🔢 <b>Código:</b> {profesor.id_profesor}
                📧 <b>Email:</b> {profesor.email}
                🏢 <b>Departamento:</b> {profesor.especialidad}
                """
                self.professor_info_label.setText(profesor_text.strip())
            else:
                self.professor_info_label.setText("Profesor no encontrado en el sistema")
        else:
            self.professor_info_label.setText("Sin profesor asignado")
        
        # Calcular y mostrar estadísticas
        promedio = self.sistema.calcular_promedio_asignatura(codigo)
        notas_asignatura = [n for n in self.sistema.notas_heap if n.asignatura == codigo]
        
        if promedio > 0:
            self.subject_avg_label.setText(f"📊 Promedio: {promedio:.2f}")
            self.subject_progress_bar.setValue(int(promedio * 10))
            
            # Determinar estado
            if promedio >= 4.5:
                estado = "🌟 Excelente rendimiento"
                color_style = "background-color: #28a745; color: white;"
            elif promedio >= 4.0:
                estado = "✅ Buen rendimiento"
                color_style = "background-color: #007bff; color: white;"
            elif promedio >= 3.0:
                estado = "⚠️ Rendimiento regular"
                color_style = "background-color: #ffc107; color: black;"
            else:
                estado = "❌ Necesita atención"
                color_style = "background-color: #dc3545; color: white;"
            
            self.subject_status_label.setText(f"🎯 Estado: {estado}")
            self.subject_status_label.setStyleSheet(f"padding: 8px; border-radius: 6px; {color_style}")
            
            # Estadísticas detalladas
            total_notas = len(notas_asignatura)
            estudiantes_unicos = len(set(n.estudiante for n in notas_asignatura))
            notas_excelentes = len([n for n in notas_asignatura if n.calificacion >= 4.5])
            notas_deficientes = len([n for n in notas_asignatura if n.calificacion < 3.0])
            
            details_text = f"""
            📊 <b>Total de calificaciones:</b> {total_notas}
            👥 <b>Estudiantes evaluados:</b> {estudiantes_unicos}
            🌟 <b>Calificaciones excelentes:</b> {notas_excelentes} ({(notas_excelentes/total_notas*100):.1f}%)
            ❌ <b>Calificaciones deficientes:</b> {notas_deficientes} ({(notas_deficientes/total_notas*100):.1f}%)
            📈 <b>Tasa de aprobación:</b> {((total_notas - notas_deficientes) / total_notas * 100):.1f}%
            """
            
            self.subject_details_label.setText(details_text.strip())
        else:
            self.subject_avg_label.setText("📊 Promedio: Sin calificaciones")
            self.subject_progress_bar.setValue(0)
            self.subject_status_label.setText("🎯 Estado: Sin evaluar")
            self.subject_status_label.setStyleSheet("padding: 8px; border-radius: 6px; background-color: #6c757d; color: white;")
            self.subject_details_label.setText("📈 Sin calificaciones registradas para esta asignatura")

    def clear_subject_stats(self):
        """Limpiar estadísticas de la asignatura"""
        self.subject_avg_label.setText("📊 Promedio: --")
        self.subject_progress_bar.setValue(0)
        self.subject_status_label.setText("🎯 Estado: --")
        self.subject_status_label.setStyleSheet("padding: 8px; border-radius: 6px; background-color: #6c757d; color: white;")
        self.subject_details_label.setText("📈 Estadísticas: --")
        self.professor_info_label.setText("Sin información disponible")

    def refresh_data(self):
        """Actualizar todos los datos"""
        self.update_table()
        self.update_statistics()
        
        # Mostrar mensaje de confirmación
        self.parent.statusBar().showMessage("🔄 Datos de asignaturas actualizados", 2000)

    def edit_subject(self):
        """Editar asignatura seleccionada"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione una asignatura para editar.")
            return
        
        codigo = self.table.item(selected, 0).text()
        asignatura = self.sistema.asignaturas.get(codigo)
        if asignatura:
            self.parent.show_edit_subject_dialog(asignatura)

    def delete_subject(self):
        """Eliminar asignatura seleccionada"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione una asignatura para eliminar.")
            return
        
        codigo = self.table.item(selected, 0).text()
        nombre = self.table.item(selected, 1).text()
        
        # Verificar si tiene calificaciones
        notas_asignatura = [n for n in self.sistema.notas_heap if n.asignatura == codigo]
        
        warning_text = f"¿Está seguro que desea eliminar la asignatura? " \
                      f"📚 Nombre: {nombre} " \
                      f"🔢 Código: {codigo} "
        
        if notas_asignatura:
            warning_text += f"⚠️ ADVERTENCIA: Esta asignatura tiene {len(notas_asignatura)} calificaciones registradas. " \
                           f"Al eliminarla, también se eliminarán todas sus calificaciones. "
        
        warning_text += "Esta acción no se puede deshacer."
        
        reply = QMessageBox.question(
            self, "🗑️ Confirmar Eliminación", 
            warning_text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.sistema.eliminar_asignatura(codigo):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Asignatura '{nombre}' eliminada correctamente.")
                self.refresh_data()
                self.parent.dashboard.update_stats()
                self.parent.update_system_info()
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  "No se pudo eliminar la asignatura.")

    def view_subject_grades(self):
        """Ver calificaciones de la asignatura seleccionada"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione una asignatura para ver sus calificaciones.")
            return
        
        codigo = self.table.item(selected, 0).text()
        nombre = self.table.item(selected, 1).text()
        
        # Ir a la pestaña de notas y filtrar por la asignatura
        self.parent.show_main_tab(3)  # Pestaña de notas
        
        # Configurar filtro en la pestaña de notas
        notes_tab = self.parent.notes_tab
        notes_tab.subject_filter.setCurrentText(nombre)
        
        self.parent.statusBar().showMessage(f"📊 Mostrando calificaciones de {nombre}", 3000)

    def assign_professor(self):
        """Asignar profesor a la asignatura seleccionada"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione una asignatura para asignar profesor.")
            return
        
        codigo = self.table.item(selected, 0).text()
        nombre = self.table.item(selected, 1).text()
        
        # Mostrar diálogo de selección de profesor
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("👨‍🏫 Asignar Profesor")
        dialog.setModal(True)
        dialog.resize(400, 200)
        
        layout = QVBoxLayout()
        
        # Información de la asignatura
        info_label = QLabel(f"📚 Asignatura: {nombre} ({codigo})")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px; margin: 10px;")
        
        # Selector de profesor
        professor_label = QLabel("👨‍🏫 Seleccionar Profesor:")
        professor_label.setStyleSheet("font-weight: bold; margin: 5px;")
        
        professor_combo = QComboBox()
        professor_combo.addItem("Sin asignar", "")
        
        # Agregar profesores disponibles
        for profesor in sorted(self.sistema.profesores.values(), key=lambda x: x.nombre):
            professor_combo.addItem(f"{profesor.nombre} - {profesor.departamento}", profesor.codigo)
        
        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addWidget(info_label)
        layout.addWidget(professor_label)
        layout.addWidget(professor_combo)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            nuevo_profesor = professor_combo.currentData()
            asignatura = self.sistema.asignaturas.get(codigo)
            
            if asignatura:
                asignatura.profesor = nuevo_profesor
                profesor_nombre = professor_combo.currentText().split(" - ")[0] if nuevo_profesor else "Sin asignar"
                
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Profesor asignado correctamente: "
                                      f"📚 Asignatura: {nombre}"
                                      f"👨‍🏫 Profesor: {profesor_nombre}")
                
                self.refresh_data()
                self.parent.dashboard.update_stats()