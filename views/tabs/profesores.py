from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
                            QLabel, QFrame, QLineEdit, QComboBox, QGroupBox, QGridLayout,
                            QSplitter, QScrollArea, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPalette

class ProfesoresTab(QWidget):
    """Pestaña de gestión de profesores con diseño moderno"""
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
        
        # Sección de acciones (toolbar original pero mejorado)
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
        
        title_label = QLabel("👨‍🏫 Gestión de Profesores")
        title_label.setObjectName("titleLabel")
        
        # Contador de profesores
        self.professors_count_label = QLabel("0 profesores registrados")
        self.professors_count_label.setObjectName("countLabel")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.professors_count_label)
        
        # Estadísticas rápidas
        stats_layout = QHBoxLayout()
        
        self.specialties_count_label = QLabel("🎓 Especialidades: --")
        self.specialties_count_label.setObjectName("statLabel")
        
        self.assigned_professors_label = QLabel("📚 Con Asignaturas: --")
        self.assigned_professors_label.setObjectName("statLabel")
        
        self.with_email_label = QLabel("📧 Con Email: --")
        self.with_email_label.setObjectName("statLabel")
        
        self.with_phone_label = QLabel("📱 Con Teléfono: --")
        self.with_phone_label.setObjectName("statLabel")
        
        stats_layout.addWidget(self.specialties_count_label)
        stats_layout.addWidget(self.assigned_professors_label)
        stats_layout.addWidget(self.with_email_label)
        stats_layout.addWidget(self.with_phone_label)
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
        self.search_input.setPlaceholderText("Buscar por ID, nombre, email o especialidad...")
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_table)
        
        # Filtro por especialidad
        specialty_label = QLabel("🎓 Especialidad:")
        specialty_label.setObjectName("filterLabel")
        
        self.specialty_filter = QComboBox()
        self.specialty_filter.setObjectName("filterCombo")
        self.specialty_filter.currentTextChanged.connect(self.filter_table)
        
        # Filtro por estado
        status_label = QLabel("📊 Estado:")
        status_label.setObjectName("filterLabel")
        
        self.status_filter = QComboBox()
        self.status_filter.setObjectName("filterCombo")
        self.status_filter.addItems(["Todos", "Con Asignaturas", "Sin Asignaturas", "Con Email", "Sin Email"])
        self.status_filter.currentTextChanged.connect(self.filter_table)
        
        # Botón limpiar filtros
        clear_filters_btn = QPushButton("🗑️ Limpiar")
        clear_filters_btn.setObjectName("clearButton")
        clear_filters_btn.clicked.connect(self.clear_filters)
        
        # Organizar elementos
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(specialty_label)
        filter_layout.addWidget(self.specialty_filter, 1)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter, 1)
        filter_layout.addWidget(clear_filters_btn)
        
        parent_layout.addWidget(filter_frame)

    def create_main_content_section(self, parent_layout):
        """Crear sección principal con tabla y panel de información"""
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Tabla de profesores (manteniendo estructura original)
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de la tabla
        table_title = QLabel("📋 Lista de Profesores")
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Tabla original pero con estilos mejorados
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["🔢 ID", "👨‍🏫 Nombre", "📧 Email", "📱 Teléfono", "🎓 Especialidad"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setObjectName("professorsTable")
        
        # Conectar doble clic para editar
        self.table.doubleClicked.connect(self.show_edit_dialog)
        
        table_layout.addWidget(self.table)
        
        # Panel derecho - Información del profesor
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setFixedWidth(350)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        # Información del profesor seleccionado
        self.create_professor_info_panel(info_layout)
        
        # Asignaturas del profesor
        self.create_subjects_panel(info_layout)
        
        # Agregar al splitter
        content_splitter.addWidget(table_frame)
        content_splitter.addWidget(info_frame)
        content_splitter.setSizes([750, 350])
        
        parent_layout.addWidget(content_splitter)

    def create_professor_info_panel(self, parent_layout):
        """Crear panel de información del profesor seleccionado"""
        info_group = QGroupBox("👨‍🏫 Información del Profesor")
        info_group.setObjectName("infoGroup")
        info_layout = QVBoxLayout(info_group)
        
        self.selected_professor_info = QLabel("Seleccione un profesor para ver detalles")
        self.selected_professor_info.setObjectName("professorInfo")
        self.selected_professor_info.setWordWrap(True)
        
        info_layout.addWidget(self.selected_professor_info)
        
        # Conectar selección de tabla
        self.table.itemSelectionChanged.connect(self.update_selected_professor_info)
        
        parent_layout.addWidget(info_group)

    def create_subjects_panel(self, parent_layout):
        """Crear panel de asignaturas del profesor"""
        subjects_group = QGroupBox("📚 Asignaturas Asignadas")
        subjects_group.setObjectName("subjectsGroup")
        subjects_layout = QVBoxLayout(subjects_group)
        
        # Contador de asignaturas
        self.professor_subjects_count = QLabel("📊 Total: 0 asignaturas")
        self.professor_subjects_count.setObjectName("subjectsCount")
        
        # Lista de asignaturas
        self.professor_subjects_list = QLabel("Sin asignaturas asignadas")
        self.professor_subjects_list.setObjectName("subjectsList")
        self.professor_subjects_list.setWordWrap(True)
        
        subjects_layout.addWidget(self.professor_subjects_count)
        subjects_layout.addWidget(self.professor_subjects_list)
        
        parent_layout.addWidget(subjects_group)
        parent_layout.addStretch()

    def create_action_section(self, parent_layout):
        """Crear sección de botones de acción (toolbar original mejorado)"""
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botones originales pero con estilos mejorados
        self.add_btn = QPushButton("➕ Agregar Profesor")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.show_add_dialog)
        
        self.edit_btn = QPushButton("✏️ Editar Profesor")
        self.edit_btn.setObjectName("secondaryButton")
        self.edit_btn.clicked.connect(self.show_edit_dialog)
        
        self.delete_btn = QPushButton("🗑️ Eliminar Profesor")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.clicked.connect(self.delete_profesor)
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setObjectName("secondaryButton")
        self.refresh_btn.clicked.connect(self.update_table)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("🏠 Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(lambda: self.parent.show_dashboard() if hasattr(self.parent, 'show_dashboard') else None)
        
        # Organizar botones (manteniendo estructura original)
        action_layout.addWidget(self.add_btn)
        action_layout.addWidget(self.edit_btn)
        action_layout.addWidget(self.delete_btn)
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
            
            #professorsTable {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #e9ecef;
            }
            
            #professorsTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            
            #professorsTable::item:selected {
                background-color: #667eea;
                color: black;
            }
            
            #professorsTable::item:hover {
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
            
            #infoGroup, #subjectsGroup {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            
            #professorInfo, #subjectsList {
                color: #495057;
                font-size: 13px;
                line-height: 1.4;
                padding: 10px;
            }
            
            #subjectsCount {
                color: #2c3e50;
                font-size: 13px;
                font-weight: bold;
                margin: 5px 0;
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

    # Métodos originales mantenidos exactamente igual
    def update_table(self):
        """Actualizar tabla con todos los profesores (método original mejorado)"""
        self.table.setRowCount(0)
        
        # Actualizar filtros
        self.update_filter_combos()
        
        # Lógica original mantenida
        profesores = sorted(self.sistema.obtener_profesores(), key=lambda x: x.nombre)
        
        for profesor in profesores:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Determinar estado del profesor para colores
            asignaturas_asignadas = [a for a in self.sistema.asignaturas.values() if hasattr(a, 'profesor') and a.profesor == profesor.id_profesor]
            
            # Validar email
            email_valido = "@" in profesor.email if profesor.email else False
            email_display = profesor.email if email_valido else "Sin email"
            email_color = QColor(46, 204, 113) if email_valido else QColor(231, 76, 60)
            
            # Items originales mantenidos
            items = [
                QTableWidgetItem(profesor.id_profesor),
                QTableWidgetItem(profesor.nombre),
                QTableWidgetItem(email_display),
                QTableWidgetItem(profesor.telefono),
                QTableWidgetItem(profesor.especialidad)
            ]
            
            # Aplicar colores mejorados
            items[2].setForeground(QBrush(email_color))
            items[2].setFont(QFont("Arial", 9, QFont.Bold if email_valido else QFont.Normal))
            
            for col, item in enumerate(items):
                self.table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        
        # Actualizar estadísticas
        self.update_statistics()

    def update_filter_combos(self):
        """Actualizar los combos de filtro"""
        # Guardar selección actual
        current_specialty = self.specialty_filter.currentText()
        
        # Limpiar combo
        self.specialty_filter.clear()
        self.specialty_filter.addItem("Todas las especialidades")
        
        # Obtener especialidades únicas
        especialidades = set()
        for profesor in self.sistema.profesores.values():
            if profesor.especialidad:
                especialidades.add(profesor.especialidad)
        
        # Agregar especialidades ordenadas
        for especialidad in sorted(especialidades):
            self.specialty_filter.addItem(especialidad)
        
        # Restaurar selección si existe
        spec_index = self.specialty_filter.findText(current_specialty)
        if spec_index >= 0:
            self.specialty_filter.setCurrentIndex(spec_index)

    def filter_table(self):
        """Filtrar tabla según criterios seleccionados"""
        search_text = self.search_input.text().lower()
        selected_specialty = self.specialty_filter.currentText()
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
            
            # Filtro por especialidad
            if selected_specialty != "Todas las especialidades":
                specialty_item = self.table.item(row, 4)
                if specialty_item and specialty_item.text() != selected_specialty:
                    show_row = False
            
            # Filtro por estado
            if selected_status != "Todos":
                id_profesor = self.table.item(row, 0).text()
                email_item = self.table.item(row, 2)
                
                if email_item:
                    has_subjects = any(hasattr(a, 'profesor') and a.profesor == id_profesor for a in self.sistema.asignaturas.values())
                    has_email = "Sin email" not in email_item.text()
                    
                    if selected_status == "Con Asignaturas" and not has_subjects:
                        show_row = False
                    elif selected_status == "Sin Asignaturas" and has_subjects:
                        show_row = False
                    elif selected_status == "Con Email" and not has_email:
                        show_row = False
                    elif selected_status == "Sin Email" and has_email:
                        show_row = False
            
            self.table.setRowHidden(row, not show_row)

    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.search_input.clear()
        self.specialty_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)

    def update_statistics(self):
        """Actualizar estadísticas generales"""
        profesores = list(self.sistema.profesores.values())
        
        if not profesores:
            self.professors_count_label.setText("0 profesores registrados")
            self.specialties_count_label.setText("🎓 Especialidades: --")
            self.assigned_professors_label.setText("📚 Con Asignaturas: --")
            self.with_email_label.setText("📧 Con Email: --")
            self.with_phone_label.setText("📱 Con Teléfono: --")
            return
        
        # Actualizar contador
        self.professors_count_label.setText(f"{len(profesores)} profesores registrados")
        
        # Contar especialidades únicas
        especialidades = set(p.especialidad for p in profesores if p.especialidad)
        self.specialties_count_label.setText(f"🎓 Especialidades: {len(especialidades)}")
        
        # Contar profesores con asignaturas
        profesores_con_asignaturas = 0
        for profesor in profesores:
            if any(hasattr(a, 'profesor') and a.profesor == profesor.id_profesor for a in self.sistema.asignaturas.values()):
                profesores_con_asignaturas += 1
        
        self.assigned_professors_label.setText(f"📚 Con Asignaturas: {profesores_con_asignaturas}")
        
        # Contar profesores con email
        profesores_con_email = sum(1 for p in profesores if p.email and "@" in p.email)
        self.with_email_label.setText(f"📧 Con Email: {profesores_con_email}")
        
        # Contar profesores con teléfono
        profesores_con_telefono = sum(1 for p in profesores if p.telefono)
        self.with_phone_label.setText(f"📱 Con Teléfono: {profesores_con_telefono}")

    def update_selected_professor_info(self):
        """Actualizar información del profesor seleccionado"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            self.selected_professor_info.setText("Seleccione un profesor para ver detalles")
            self.professor_subjects_count.setText("📊 Total: 0 asignaturas")
            self.professor_subjects_list.setText("Sin asignaturas asignadas")
            return
        
        # Obtener información del profesor
        id_profesor = self.table.item(selected_row, 0).text()
        profesor = self.sistema.profesores.get(id_profesor)
        
        if not profesor:
            return
        
        # Información básica
        info_text = f"""
        🔢 <b>ID:</b> {profesor.id_profesor}
        👨‍🏫 <b>Nombre:</b> {profesor.nombre}
        📧 <b>Email:</b> {profesor.email if profesor.email else 'Sin email'}
        📱 <b>Teléfono:</b> {profesor.telefono if profesor.telefono else 'Sin teléfono'}
        🎓 <b>Especialidad:</b> {profesor.especialidad if profesor.especialidad else 'Sin especialidad'}
        """
        self.selected_professor_info.setText(info_text.strip())
        
        # Obtener asignaturas del profesor
        asignaturas_profesor = [a for a in self.sistema.asignaturas.values() if hasattr(a, 'profesor') and a.profesor == id_profesor]
        
        if asignaturas_profesor:
            self.professor_subjects_count.setText(f"📊 Total: {len(asignaturas_profesor)} asignaturas")
            
            # Lista de asignaturas
            asignaturas_text = ""
            for asignatura in sorted(asignaturas_profesor, key=lambda x: x.nombre):
                creditos_text = f" - {asignatura.creditos} créditos" if hasattr(asignatura, 'creditos') else ""
                asignaturas_text += f"📚 <b>{asignatura.nombre}</b> ({asignatura.codigo}){creditos_text}\n"
            
            self.professor_subjects_list.setText(asignaturas_text.strip())
        else:
            self.professor_subjects_count.setText("📊 Total: 0 asignaturas")
            self.professor_subjects_list.setText("Sin asignaturas asignadas")

    # Métodos originales mantenidos exactamente igual
    def show_add_dialog(self):
        try:
            from ..dialogs.profesor import ProfesorDialog
            dialog = ProfesorDialog(parent=self.parent)
            if dialog.exec_() == QDialog.Accepted:
                from models.profesor import Profesor
                data = dialog.get_data()
                
                if not data['id_profesor'] or not data['nombre']:
                    QMessageBox.warning(self, "⚠️ Error", "ID y nombre son campos obligatorios")
                    return
                    
                nuevo_profesor = Profesor(
                    data['id_profesor'],
                    data['nombre'],
                    data['email'],
                    data['telefono'],
                    data['especialidad']
                )
                
                if self.sistema.agregar_profesor(nuevo_profesor):
                    QMessageBox.information(self, "✅ Éxito", "Profesor agregado correctamente")
                    self.update_table()
                else:
                    QMessageBox.warning(self, "❌ Error", "El ID de profesor ya existe")
        except ImportError:
            QMessageBox.warning(self, "❌ Error", "No se pudo cargar el diálogo de profesor")

    def show_edit_dialog(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Error", "Seleccione un profesor para editar")
            return
        
        id_profesor = self.table.item(selected, 0).text()
        profesor = self.sistema.profesores.get(id_profesor)
        
        if profesor:
            try:
                from ..dialogs.profesor import ProfesorDialog
                dialog = ProfesorDialog(profesor, self.parent)
                if dialog.exec_() == QDialog.Accepted:
                    from models.profesor import Profesor
                    data = dialog.get_data()
                    
                    if not data['id_profesor'] or not data['nombre']:
                        QMessageBox.warning(self, "⚠️ Error", "ID y nombre son campos obligatorios")
                        return
                        
                    profesor_editado = Profesor(
                        data['id_profesor'],
                        data['nombre'],
                        data['email'],
                        data['telefono'],
                        data['especialidad']
                    )
                    
                    if self.sistema.editar_profesor(id_profesor, profesor_editado):
                        QMessageBox.information(self, "✅ Éxito", "Profesor actualizado correctamente")
                        self.update_table()
                    else:
                        QMessageBox.warning(self, "❌ Error", "No se pudo actualizar el profesor")
            except ImportError:
                QMessageBox.warning(self, "❌ Error", "No se pudo cargar el diálogo de profesor")

    def delete_profesor(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "⚠️ Error", "Seleccione un profesor para eliminar")
            return
        
        id_profesor = self.table.item(selected, 0).text()
        profesor = self.sistema.profesores.get(id_profesor)
        
        if profesor:
            reply = QMessageBox.question(
                self, "🗑️ Confirmar", 
                f"¿Está seguro que desea eliminar al profesor {profesor.nombre}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.sistema.eliminar_profesor(id_profesor):
                    QMessageBox.information(self, "✅ Éxito", "Profesor eliminado correctamente")
                    self.update_table()
                else:
                    QMessageBox.warning(self, "❌ Error", 
                        "No se pudo eliminar el profesor. Verifique que no esté asignado a ninguna asignatura.")