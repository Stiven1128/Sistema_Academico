from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                            QLabel, QFrame, QLineEdit, QComboBox, QGroupBox, QGridLayout,
                            QSplitter, QScrollArea, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPalette

class StudentsTab(QWidget):
    """Pestaña de gestión de estudiantes con diseño moderno"""
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
        
        # Sección principal con tabla y información del estudiante
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
        
        title_label = QLabel("👥 Gestión de Estudiantes")
        title_label.setObjectName("titleLabel")
        
        # Contador de estudiantes
        self.students_count_label = QLabel("0 estudiantes registrados")
        self.students_count_label.setObjectName("countLabel")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.students_count_label)
        
        # Estadísticas rápidas
        stats_layout = QHBoxLayout()
        
        self.programs_count_label = QLabel("📚 Programas: --")
        self.programs_count_label.setObjectName("statLabel")
        
        self.avg_grade_label = QLabel("📊 Promedio General: --")
        self.avg_grade_label.setObjectName("statLabel")
        
        self.risk_students_label = QLabel("⚠️ En Riesgo: --")
        self.risk_students_label.setObjectName("statLabel")
        
        self.excellent_students_label = QLabel("🌟 Excelentes: --")
        self.excellent_students_label.setObjectName("statLabel")
        
        stats_layout.addWidget(self.programs_count_label)
        stats_layout.addWidget(self.avg_grade_label)
        stats_layout.addWidget(self.risk_students_label)
        stats_layout.addWidget(self.excellent_students_label)
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
        self.search_input.setPlaceholderText("Buscar por código, nombre, programa o email...")
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_table)
        
        # Filtro por programa
        program_label = QLabel("📚 Programa:")
        program_label.setObjectName("filterLabel")
        
        self.program_filter = QComboBox()
        self.program_filter.setObjectName("filterCombo")
        self.program_filter.currentTextChanged.connect(self.filter_table)
        
        # Filtro por rendimiento académico
        performance_label = QLabel("📈 Rendimiento:")
        performance_label.setObjectName("filterLabel")
        
        self.performance_filter = QComboBox()
        self.performance_filter.setObjectName("filterCombo")
        self.performance_filter.addItems(["Todos", "Excelente (≥4.5)", "Bueno (4.0-4.4)", 
                                         "Regular (3.0-3.9)", "En Riesgo (<3.0)", "Sin Calificaciones"])
        self.performance_filter.currentTextChanged.connect(self.filter_table)
        
        # Botón limpiar filtros
        clear_filters_btn = QPushButton("🗑️ Limpiar")
        clear_filters_btn.setObjectName("clearButton")
        clear_filters_btn.clicked.connect(self.clear_filters)
        
        # Organizar elementos
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(program_label)
        filter_layout.addWidget(self.program_filter, 1)
        filter_layout.addWidget(performance_label)
        filter_layout.addWidget(self.performance_filter, 1)
        filter_layout.addWidget(clear_filters_btn)
        
        parent_layout.addWidget(filter_frame)
    
    def create_main_content_section(self, parent_layout):
        """Crear sección principal con tabla y panel de información"""
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Tabla de estudiantes
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de la tabla
        table_title = QLabel("📋 Lista de Estudiantes")
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Tabla de estudiantes mejorada
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "🔢 Código", "👤 Nombre", "📚 Programa", 
            "📧 Email", "📱 Teléfono", "📊 Promedio"
        ])
        
        # Configurar tabla
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Nombre
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Programa
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)  # Email
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setObjectName("studentsTable")
        
        # Conectar doble clic para editar
        self.table.doubleClicked.connect(self.edit_student)
        
        table_layout.addWidget(self.table)
        
        # Panel derecho - Información del estudiante
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setFixedWidth(350)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        # Información del estudiante seleccionado
        self.create_student_info_panel(info_layout)
        
        # Rendimiento académico del estudiante
        self.create_performance_panel(info_layout)
        
        # Agregar al splitter
        content_splitter.addWidget(table_frame)
        content_splitter.addWidget(info_frame)
        content_splitter.setSizes([750, 350])
        
        parent_layout.addWidget(content_splitter)
    
    def create_student_info_panel(self, parent_layout):
        """Crear panel de información del estudiante seleccionado"""
        info_group = QGroupBox("👤 Información del Estudiante")
        info_group.setObjectName("infoGroup")
        info_layout = QGridLayout(info_group)  # Cambiado a QGridLayout para mejor organización
        
        # Estilo para las etiquetas de información
        self.selected_student_info = QLabel("Seleccione un estudiante para ver detalles")
        self.selected_student_info.setObjectName("studentInfo")
        self.selected_student_info.setWordWrap(True)
        self.selected_student_info.setStyleSheet("color: black;")
        
        info_layout.addWidget(self.selected_student_info, 0, 0, 1, 2)
        
        # Conectar selección de tabla
        self.table.itemSelectionChanged.connect(self.update_selected_student_info)
        
        parent_layout.addWidget(info_group)

    def create_performance_panel(self, parent_layout):
        """Crear panel de rendimiento académico"""
        performance_group = QGroupBox("📈 Rendimiento Académico")
        performance_group.setObjectName("performanceGroup")
        performance_layout = QGridLayout(performance_group)  # Cambiado a QGridLayout
        
        # Promedio del estudiante
        self.student_avg_label = QLabel("📊 Promedio: --")
        self.student_avg_label.setObjectName("performanceLabel")
        self.student_avg_label.setStyleSheet("color: black; font-weight: bold;")
        performance_layout.addWidget(self.student_avg_label, 0, 0, 1, 2)
        
        # Barra de progreso visual
        self.performance_bar = QProgressBar()
        self.performance_bar.setRange(0, 50)  # 0 a 5.0 * 10
        self.performance_bar.setValue(0)
        self.performance_bar.setObjectName("performanceBar")
        performance_layout.addWidget(self.performance_bar, 1, 0, 1, 2)
        
        # Estado académico
        self.academic_status_label = QLabel("🎯 Estado: --")
        self.academic_status_label.setObjectName("statusLabel")
        self.academic_status_label.setStyleSheet("color: black; font-weight: bold;")
        performance_layout.addWidget(self.academic_status_label, 2, 0, 1, 2)
        
        # Título de estadísticas
        stats_title = QLabel("📋 Estadísticas de Calificaciones:")
        stats_title.setStyleSheet("color: black; font-weight: bold;")
        performance_layout.addWidget(stats_title, 3, 0, 1, 2)
        
        # Estadísticas de calificaciones (ahora en una tabla)
        self.grade_stats_label = QLabel()
        self.grade_stats_label.setObjectName("gradeStats")
        self.grade_stats_label.setWordWrap(True)
        self.grade_stats_label.setStyleSheet("color: black;")
        performance_layout.addWidget(self.grade_stats_label, 4, 0, 1, 2)
        
        parent_layout.addWidget(performance_group)
        parent_layout.addStretch()
    
    def create_action_section(self, parent_layout):
        """Crear sección de botones de acción"""
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botones principales
        self.add_student_btn = QPushButton("➕ Nuevo Estudiante")
        self.add_student_btn.setObjectName("primaryButton")
        self.add_student_btn.clicked.connect(self.parent.show_add_student_dialog)
        
        self.edit_student_btn = QPushButton("✏️ Editar")
        self.edit_student_btn.setObjectName("secondaryButton")
        self.edit_student_btn.clicked.connect(self.edit_student)
        
        self.delete_student_btn = QPushButton("🗑️ Eliminar")
        self.delete_student_btn.setObjectName("dangerButton")
        self.delete_student_btn.clicked.connect(self.delete_student)
        
        self.view_grades_btn = QPushButton("📊 Ver Calificaciones")
        self.view_grades_btn.setObjectName("infoButton")
        self.view_grades_btn.clicked.connect(self.view_student_grades)
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setObjectName("secondaryButton")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("🏠 Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.parent.show_dashboard)
        
        # Organizar botones
        action_layout.addWidget(self.add_student_btn)
        action_layout.addWidget(self.edit_student_btn)
        action_layout.addWidget(self.delete_student_btn)
        action_layout.addWidget(self.view_grades_btn)
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
                color: black;
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
                border-color: #4facfe;
                background-color: white;
            }
            
            #filterCombo {
                padding: 6px 10px;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                min-width: 140px;
            }
            
            #filterCombo:focus {
                border-color: #4facfe;
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
            
            #studentsTable {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #e9ecef;
            }
            
            #studentsTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            
            #studentsTable::item:selected {
                background-color: #4facfe;
                color: white;
            }
            
            #studentsTable::item:hover {
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
            
            #infoGroup, #performanceGroup {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            
            #studentInfo, #gradeStats {
                color: #495057;
                font-size: 13px;
                line-height: 1.4;
                padding: 10px;
            }
            
            #performanceLabel, #statusLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                margin: 5px 0;
            }
            
            #performanceBar {
                height: 20px;
                border-radius: 10px;
                background-color: #e9ecef;
                margin: 5px 0;
            }
            
            #performanceBar::chunk {
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
                    stop:0 #4facfe, stop:1 #00f2fe);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #secondaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #007bff);
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
        """Actualizar tabla con todos los estudiantes"""
        self.table.setRowCount(0)
        
        # Actualizar filtros
        self.update_filter_combos()
        
        # Obtener estudiantes ordenados
        estudiantes = sorted(self.sistema.obtener_estudiantes(), key=lambda x: x.nombre)
        
        for estudiante in estudiantes:
            self.add_student_to_table(estudiante)
        
        # Actualizar contador
        self.students_count_label.setText(f"{len(estudiantes)} estudiantes registrados")
    
    def add_student_to_table(self, estudiante):
        """Agregar un estudiante a la tabla"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Calcular promedio del estudiante
        promedio = self.sistema.calcular_promedio_estudiante(estudiante.codigo)
        promedio_str = f"{promedio:.2f}" if promedio > 0 else "Sin notas"
        
        # Determinar color del promedio
        if promedio >= 4.5:
            promedio_color = QColor(46, 204, 113)  # Verde
        elif promedio >= 4.0:
            promedio_color = QColor(52, 152, 219)  # Azul
        elif promedio >= 3.0:
            promedio_color = QColor(241, 196, 15)  # Amarillo
        elif promedio > 0:
            promedio_color = QColor(231, 76, 60)  # Rojo
        else:
            promedio_color = QColor(108, 117, 125)  # Gris
        
        # Crear items para la tabla
        items = [
            QTableWidgetItem(estudiante.codigo),
            QTableWidgetItem(estudiante.nombre),
            QTableWidgetItem(estudiante.programa),
            QTableWidgetItem(estudiante.email),
            QTableWidgetItem(estudiante.telefono),
            QTableWidgetItem(promedio_str)
        ]
        
        # Aplicar formato especial al promedio
        items[5].setForeground(QBrush(promedio_color))
        items[5].setFont(QFont("Arial", 10, QFont.Bold))
        
        # Hacer celdas no editables
        for col, item in enumerate(items):
            self.table.setItem(row, col, item)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def update_filter_combos(self):
        """Actualizar los combos de filtro"""
        # Guardar selección actual
        current_program = self.program_filter.currentText()
        
        # Limpiar combo
        self.program_filter.clear()
        
        # Agregar opción "Todos"
        self.program_filter.addItem("Todos los programas")
        
        # Obtener programas únicos
        programas = set()
        for estudiante in self.sistema.estudiantes.values():
            programas.add(estudiante.programa)
        
        # Agregar programas ordenados
        for programa in sorted(programas):
            self.program_filter.addItem(programa)
        
        # Restaurar selección si existe
        program_index = self.program_filter.findText(current_program)
        if program_index >= 0:
            self.program_filter.setCurrentIndex(program_index)
    
    def filter_table(self):
        """Filtrar tabla según criterios seleccionados"""
        search_text = self.search_input.text().lower()
        selected_program = self.program_filter.currentText()
        selected_performance = self.performance_filter.currentText()
        
        for row in range(self.table.rowCount()):
            show_row = True
            
            # Filtro por texto de búsqueda
            if search_text:
                row_text = ""
                for col in range(self.table.columnCount() - 1):  # Excluir promedio
                    item = self.table.item(row, col)
                    if item:
                        row_text += item.text().lower() + " "
                
                if search_text not in row_text:
                    show_row = False
            
            # Filtro por programa
            if selected_program != "Todos los programas":
                program_item = self.table.item(row, 2)
                if program_item and program_item.text() != selected_program:
                    show_row = False
            
            # Filtro por rendimiento
            if selected_performance != "Todos":
                promedio_item = self.table.item(row, 5)
                if promedio_item:
                    promedio_text = promedio_item.text()
                    if promedio_text == "Sin notas":
                        if selected_performance != "Sin Calificaciones":
                            show_row = False
                    else:
                        try:
                            promedio = float(promedio_text)
                            if selected_performance == "Excelente (≥4.5)" and promedio < 4.5:
                                show_row = False
                            elif selected_performance == "Bueno (4.0-4.4)" and not (4.0 <= promedio < 4.5):
                                show_row = False
                            elif selected_performance == "Regular (3.0-3.9)" and not (3.0 <= promedio < 4.0):
                                show_row = False
                            elif selected_performance == "En Riesgo (<3.0)" and promedio >= 3.0:
                                show_row = False
                            elif selected_performance == "Sin Calificaciones":
                                show_row = False
                        except ValueError:
                            if selected_performance != "Sin Calificaciones":
                                show_row = False
            
            self.table.setRowHidden(row, not show_row)
    
    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.search_input.clear()
        self.program_filter.setCurrentIndex(0)
        self.performance_filter.setCurrentIndex(0)
    
    def update_statistics(self):
        """Actualizar estadísticas generales"""
        estudiantes = list(self.sistema.estudiantes.values())
        
        if not estudiantes:
            self.programs_count_label.setText("📚 Programas: --")
            self.avg_grade_label.setText("📊 Promedio General: --")
            self.risk_students_label.setText("⚠️ En Riesgo: --")
            self.excellent_students_label.setText("🌟 Excelentes: --")
            return
        
        # Contar programas únicos
        programas = set(e.programa for e in estudiantes)
        self.programs_count_label.setText(f"📚 Programas: {len(programas)}")
        
        # Calcular estadísticas de rendimiento
        promedios = []
        estudiantes_riesgo = 0
        estudiantes_excelentes = 0
        
        for estudiante in estudiantes:
            promedio = self.sistema.calcular_promedio_estudiante(estudiante.codigo)
            if promedio > 0:
                promedios.append(promedio)
                if promedio < 3.0:
                    estudiantes_riesgo += 1
                elif promedio >= 4.5:
                    estudiantes_excelentes += 1
        
        # Actualizar labels
        if promedios:
            promedio_general = sum(promedios) / len(promedios)
            self.avg_grade_label.setText(f"📊 Promedio General: {promedio_general:.2f}")
        else:
            self.avg_grade_label.setText("📊 Promedio General: Sin datos")
        
        self.risk_students_label.setText(f"⚠️ En Riesgo: {estudiantes_riesgo}")
        self.excellent_students_label.setText(f"🌟 Excelentes: {estudiantes_excelentes}")
    
    def update_selected_student_info(self):
        """Actualizar información del estudiante seleccionado"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            self.selected_student_info.setText("Seleccione un estudiante para ver detalles")
            self.student_avg_label.setText("📊 Promedio: --")
            self.performance_bar.setValue(0)
            self.academic_status_label.setText("🎯 Estado: --")
            self.grade_stats_label.setText("")
            return
        
        # Obtener información del estudiante
        codigo = self.table.item(selected_row, 0).text()
        nombre = self.table.item(selected_row, 1).text()
        programa = self.table.item(selected_row, 2).text()
        email = self.table.item(selected_row, 3).text()
        telefono = self.table.item(selected_row, 4).text()
        
        # Información básica con mejor formato
        info_text = f"""
        <table style='width:100%; color: black;'>
            <tr><td style='width:30%;'><b>🔢 Código:</b></td><td>{codigo}</td></tr>
            <tr><td><b>👤 Nombre:</b></td><td>{nombre}</td></tr>
            <tr><td><b>📚 Programa:</b></td><td>{programa}</td></tr>
            <tr><td><b>📧 Email:</b></td><td>{email}</td></tr>
            <tr><td><b>📱 Teléfono:</b></td><td>{telefono}</td></tr>
        </table>
        """
        self.selected_student_info.setText(info_text.strip())
        
        # Calcular y mostrar rendimiento
        promedio = self.sistema.calcular_promedio_estudiante(codigo)
        
        if promedio > 0:
            self.student_avg_label.setText(f"📊 Promedio: {promedio:.2f}")
            self.performance_bar.setValue(int(promedio * 10))
            
            # Determinar estado académico
            if promedio >= 4.5:
                estado = "🌟 Excelente"
                color = "background-color: #28a745; color: white;"
            elif promedio >= 4.0:
                estado = "✅ Bueno"
                color = "background-color: #007bff; color: white;"
            elif promedio >= 3.0:
                estado = "⚠️ Regular"
                color = "background-color: #ffc107; color: black;"
            else:
                estado = "❌ En Riesgo"
                color = "background-color: #dc3545; color: white;"
            
            self.academic_status_label.setText(f"🎯 Estado: {estado}")
            self.academic_status_label.setStyleSheet(f"padding: 5px; border-radius: 4px; {color}")
            
            # Estadísticas de calificaciones con mejor formato
            notas_estudiante = [n for n in self.sistema.notas_heap if n.estudiante == codigo]
            if notas_estudiante:
                total_notas = len(notas_estudiante)
                notas_excelentes = len([n for n in notas_estudiante if n.calificacion >= 4.5])
                notas_buenas = len([n for n in notas_estudiante if 4.0 <= n.calificacion < 4.5])
                notas_regulares = len([n for n in notas_estudiante if 3.0 <= n.calificacion < 4.0])
                notas_riesgo = len([n for n in notas_estudiante if n.calificacion < 3.0])
                
                stats_text = f"""
                <table style='width:100%; color: black;'>
                    <tr><td style='width:70%;'>Total de calificaciones:</td><td><b>{total_notas}</b></td></tr>
                    <tr><td>Excelentes (≥4.5):</td><td><b>{notas_excelentes}</b></td></tr>
                    <tr><td>Buenas (4.0-4.4):</td><td><b>{notas_buenas}</b></td></tr>
                    <tr><td>Regulares (3.0-3.9):</td><td><b>{notas_regulares}</b></td></tr>
                    <tr><td>En riesgo (<3.0):</td><td><b>{notas_riesgo}</b></td></tr>
                    <tr><td>Porcentaje de éxito:</td><td><b>{((total_notas - notas_riesgo) / total_notas * 100):.1f}%</b></td></tr>
                </table>
                """
                self.grade_stats_label.setText(stats_text.strip())
            else:
                self.grade_stats_label.setText("<span style='color: black;'>📋 Sin calificaciones registradas</span>")
        else:
            self.student_avg_label.setText("📊 Promedio: Sin calificaciones")
            self.performance_bar.setValue(0)
            self.academic_status_label.setText("🎯 Estado: Sin evaluar")
            self.academic_status_label.setStyleSheet("padding: 5px; border-radius: 4px; background-color: #6c757d; color: white;")
            self.grade_stats_label.setText("<span style='color: black;'>📋 Sin calificaciones registradas</span>")
        
    def refresh_data(self):
        """Actualizar todos los datos"""
        self.update_table()
        self.update_statistics()
        
        # Mostrar mensaje de confirmación
        self.parent.statusBar().showMessage("🔄 Datos de estudiantes actualizados", 2000)
    
    def edit_student(self):
        """Editar estudiante seleccionado"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione un estudiante para editar.")
            return
        
        codigo = self.table.item(selected, 0).text()
        estudiante = self.sistema.estudiantes.get(codigo)
        if estudiante:
            self.parent.show_edit_student_dialog(estudiante)
    
    def delete_student(self):
        """Eliminar estudiante seleccionado"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione un estudiante para eliminar.")
            return
        
        codigo = self.table.item(selected, 0).text()
        nombre = self.table.item(selected, 1).text()
        
        # Verificar si tiene calificaciones
        notas_estudiante = [n for n in self.sistema.notas_heap if n.estudiante == codigo]
        
        warning_text = f"¿Está seguro que desea eliminar al estudiante?\n\n" \
                      f"👤 Nombre: {nombre}\n" \
                      f"🔢 Código: {codigo}\n\n"
        
        if notas_estudiante:
            warning_text += f"⚠️ ADVERTENCIA: Este estudiante tiene {len(notas_estudiante)} calificaciones registradas.\n" \
                           f"Al eliminarlo, también se eliminarán todas sus calificaciones.\n\n"
        
        warning_text += "Esta acción no se puede deshacer."
        
        reply = QMessageBox.question(
            self, "🗑️ Confirmar Eliminación", 
            warning_text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.sistema.eliminar_estudiante(codigo):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Estudiante '{nombre}' eliminado correctamente.")
                self.refresh_data()
                self.parent.dashboard.update_stats()
                self.parent.update_system_info()
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  "No se pudo eliminar el estudiante.")
    
    def view_student_grades(self):
        """Ver calificaciones del estudiante seleccionado"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Selección Requerida", 
                              "Seleccione un estudiante para ver sus calificaciones.")
            return
        
        codigo = self.table.item(selected, 0).text()
        nombre = self.table.item(selected, 1).text()
        
        # Ir a la pestaña de notas y filtrar por el estudiante
        self.parent.show_main_tab(3)  # Pestaña de notas
        
        # Configurar filtro en la pestaña de notas
        notes_tab = self.parent.notes_tab
        notes_tab.student_filter.setCurrentText(nombre)
        
        self.parent.statusBar().showMessage(f"📊 Mostrando calificaciones de {nombre}", 3000)