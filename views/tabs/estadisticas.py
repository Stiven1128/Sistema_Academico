from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QComboBox, 
                            QTableWidget, QLabel, QHBoxLayout, QDoubleSpinBox, 
                            QPushButton, QHeaderView, QTableWidgetItem, QFrame,
                            QGridLayout, QGroupBox, QProgressBar, QScrollArea,
                            QSplitter, QLineEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont, QPalette
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import date, datetime, time

class StatsTab(QWidget):
    """Pestaña de estadísticas con diseño moderno"""
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
        
        # Header con título y estadísticas generales
        self.create_header_section(main_layout)
        
        # Pestañas internas modernas
        self.create_stats_tabs(main_layout)
        
        # Sección de acciones
        self.create_action_section(main_layout)
        
        self.setLayout(main_layout)
        
        # Actualizar datos iniciales
        self.update_all_data()
    
    def create_header_section(self, parent_layout):
        """Crear sección de encabezado con estadísticas generales"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        
        # Título principal
        title_layout = QHBoxLayout()
        
        title_label = QLabel("📊 Estadísticas y Análisis Académico")
        title_label.setObjectName("titleLabel")
        
        # Fecha de actualización
        self.last_update_label = QLabel("Última actualización: Ahora")
        self.last_update_label.setObjectName("updateLabel")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.last_update_label)
        
        # Estadísticas generales del sistema
        stats_grid = QGridLayout()
        
        # Crear cards de estadísticas
        self.total_students_card = self.create_stat_card("👥", "Estudiantes", "0", "#4facfe")
        self.total_subjects_card = self.create_stat_card("📚", "Asignaturas", "0", "#43e97b")
        self.total_grades_card = self.create_stat_card("📝", "Calificaciones", "0", "#fa709a")
        self.system_avg_card = self.create_stat_card("📊", "Promedio Sistema", "0.00", "#fee140")
        
        stats_grid.addWidget(self.total_students_card, 0, 0)
        stats_grid.addWidget(self.total_subjects_card, 0, 1)
        stats_grid.addWidget(self.total_grades_card, 0, 2)
        stats_grid.addWidget(self.system_avg_card, 0, 3)
        
        header_layout.addLayout(title_layout)
        header_layout.addLayout(stats_grid)
        
        parent_layout.addWidget(header_frame)
    
    def create_stat_card(self, icon, title, value, color):
        """Crear tarjeta de estadística con mejor organización"""
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            #statCard {{
                background: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                min-height: 80px;
                border: 1px solid #e0e0e0;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        # Encabezado con icono y título
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            color: {color};
            margin-right: 10px;
        """)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 12px;
            color: #000000;
            font-weight: bold;
        """)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        value_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 5px;
        """)
        value_label.setAlignment(Qt.AlignRight)
        
        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        
        # Guardar referencia al label del valor
        card.value_label = value_label
        
        return card
    
    def create_stats_tabs(self, parent_layout):
        """Crear pestañas de estadísticas"""
        self.stats_tabs = QTabWidget()
        self.stats_tabs.setObjectName("statsTabWidget")
        
        # Pestaña de estudiantes
        self.create_student_stats_tab()
        
        # Pestaña de asignaturas
        self.create_subject_stats_tab()
        
        # Pestaña de ranking
        self.create_ranking_tab()
        
        # Pestaña de estudiantes en riesgo
        self.create_risk_tab()
        
        # Pestaña de análisis visual
        self.create_visual_analysis_tab()
        
        parent_layout.addWidget(self.stats_tabs)
    
    def create_student_stats_tab(self):
        """Mejorar organización de la pestaña de estudiantes"""
        student_tab = QWidget()
        layout = QVBoxLayout(student_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Sección de selección
        selection_frame = QFrame()
        selection_frame.setObjectName("selectionFrame")
        selection_layout = QHBoxLayout(selection_frame)
        selection_layout.setContentsMargins(15, 10, 15, 10)
        
        selection_label = QLabel("👤 Seleccionar Estudiante:")
        selection_label.setObjectName("selectionLabel")
        
        self.student_combo = QComboBox()
        self.student_combo.setObjectName("modernCombo")
        self.student_combo.currentTextChanged.connect(self.update_student_stats)
        
        # Búsqueda rápida
        search_label = QLabel("🔍 Buscar:")
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Buscar estudiante...")
        self.student_search.setObjectName("searchInput")
        self.student_search.textChanged.connect(self.filter_students)
        
        selection_layout.addWidget(selection_label)
        selection_layout.addWidget(self.student_combo, 2)
        selection_layout.addWidget(search_label)
        selection_layout.addWidget(self.student_search, 1)
        
        # Contenido principal con splitter
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Tabla de notas
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        table_title = QLabel("📋 Calificaciones del Estudiante")
        table_title.setObjectName("sectionTitle")
        table_title.setAlignment(Qt.AlignCenter)
        
        self.student_notes_table = QTableWidget()
        self.student_notes_table.setColumnCount(5)
        self.student_notes_table.setHorizontalHeaderLabels([
            "📚 Asignatura", "📊 Calificación", "⚖️ Peso", "📅 Fecha", "🎯 Estado"
        ])
        self.student_notes_table.setObjectName("modernTable")
        self.student_notes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_notes_table.verticalHeader().setVisible(False)
        self.student_notes_table.setAlternatingRowColors(True)
        
        table_layout.addWidget(table_title)
        table_layout.addWidget(self.student_notes_table)
        
        # Panel derecho - Información del estudiante
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setFixedWidth(300)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(10)
        
        # Scroll area para la información del estudiante
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(10)
        
        # Información básica
        basic_info_group = QGroupBox("👤 Información Básica")
        basic_info_group.setObjectName("infoGroup")
        basic_info_layout = QGridLayout(basic_info_group)
        basic_info_layout.setContentsMargins(10, 15, 10, 15)
        basic_info_layout.setSpacing(5)
        
        self.student_info_label = QLabel("Seleccione un estudiante")
        self.student_info_label.setObjectName("infoText")
        self.student_info_label.setWordWrap(True)
        self.student_info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.student_info_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        basic_info_layout.addWidget(self.student_info_label)
        scroll_layout.addWidget(basic_info_group)
        
        # Estadísticas académicas
        academic_group = QGroupBox("📊 Rendimiento Académico")
        academic_group.setObjectName("infoGroup")
        academic_layout = QVBoxLayout(academic_group)
        academic_layout.setContentsMargins(10, 15, 10, 15)
        academic_layout.setSpacing(10)
        
        # Organización en grid para estadísticas
        stats_grid = QGridLayout()
        stats_grid.setSpacing(10)
        
        self.student_avg_label = QLabel("📊 Promedio Simple: --")
        self.student_avg_label.setObjectName("statText")
        self.student_avg_label.setWordWrap(True)
        
        self.student_weighted_avg_label = QLabel("⚖️ Promedio Ponderado: --")
        self.student_weighted_avg_label.setObjectName("statText")
        self.student_weighted_avg_label.setWordWrap(True)
        
        self.student_status_label = QLabel("🎯 Estado: --")
        self.student_status_label.setObjectName("statusText")
        self.student_status_label.setAlignment(Qt.AlignCenter)
        
        # Barra de progreso
        self.student_progress_bar = QProgressBar()
        self.student_progress_bar.setRange(0, 50)
        self.student_progress_bar.setObjectName("progressBar")
        
        stats_grid.addWidget(self.student_avg_label, 0, 0)
        stats_grid.addWidget(self.student_weighted_avg_label, 1, 0)
        stats_grid.addWidget(self.student_progress_bar, 2, 0)
        stats_grid.addWidget(self.student_status_label, 3, 0)
        
        academic_layout.addLayout(stats_grid)
        scroll_layout.addWidget(academic_group)
        
        # Estadísticas detalladas
        details_group = QGroupBox("📈 Estadísticas Detalladas")
        details_group.setObjectName("infoGroup")
        details_layout = QVBoxLayout(details_group)
        details_layout.setContentsMargins(10, 15, 10, 15)
        details_layout.setSpacing(5)
        
        self.student_details_label = QLabel("Sin datos disponibles")
        self.student_details_label.setObjectName("detailsText")
        self.student_details_label.setWordWrap(True)
        self.student_details_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.student_details_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        details_layout.addWidget(self.student_details_label)
        scroll_layout.addWidget(details_group)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        info_layout.addWidget(scroll_area)
        
        content_splitter.addWidget(table_frame)
        content_splitter.addWidget(info_frame)
        content_splitter.setSizes([700, 300])
        
        layout.addWidget(selection_frame)
        layout.addWidget(content_splitter)
        
        self.stats_tabs.addTab(student_tab, "👥 Estudiantes")
    
    def create_subject_stats_tab(self):
        """Crear pestaña de estadísticas de asignaturas"""
        subject_tab = QWidget()
        layout = QVBoxLayout(subject_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Sección de selección
        selection_frame = QFrame()
        selection_frame.setObjectName("selectionFrame")
        selection_layout = QHBoxLayout(selection_frame)
        selection_layout.setContentsMargins(15, 10, 15, 10)
        
        selection_label = QLabel("📚 Seleccionar Asignatura:")
        selection_label.setObjectName("selectionLabel")
        
        self.subject_combo = QComboBox()
        self.subject_combo.setObjectName("modernCombo")
        self.subject_combo.currentTextChanged.connect(self.update_subject_stats)
        
        selection_layout.addWidget(selection_label)
        selection_layout.addWidget(self.subject_combo, 2)
        selection_layout.addStretch()
        
        # Contenido principal
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Tabla de calificaciones
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        table_title = QLabel("📋 Calificaciones de la Asignatura")
        table_title.setObjectName("sectionTitle")
        
        self.subject_notes_table = QTableWidget()
        self.subject_notes_table.setColumnCount(5)
        self.subject_notes_table.setHorizontalHeaderLabels([
            "👤 Estudiante", "📊 Calificación", "⚖️ Peso", "📅 Fecha", "🎯 Estado"
        ])
        self.subject_notes_table.setObjectName("modernTable")
        self.subject_notes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subject_notes_table.verticalHeader().setVisible(False)
        self.subject_notes_table.setAlternatingRowColors(True)
        
        table_layout.addWidget(table_title)
        table_layout.addWidget(self.subject_notes_table)
        
        # Panel derecho - Estadísticas de la asignatura
        stats_frame = QFrame()
        stats_frame.setObjectName("infoFrame")
        stats_frame.setFixedWidth(300)
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 15, 15, 15)
        
        # Información de la asignatura
        subject_info_group = QGroupBox("📚 Información de la Asignatura")
        subject_info_group.setObjectName("infoGroup")
        subject_info_layout = QVBoxLayout(subject_info_group)
        
        self.subject_info_label = QLabel("Seleccione una asignatura")
        self.subject_info_label.setObjectName("infoText")
        self.subject_info_label.setWordWrap(True)
        
        subject_info_layout.addWidget(self.subject_info_label)
        
        # Estadísticas de rendimiento
        performance_group = QGroupBox("📊 Estadísticas de Rendimiento")
        performance_group.setObjectName("infoGroup")
        performance_layout = QVBoxLayout(performance_group)
        
        self.subject_avg_label = QLabel("📊 Promedio: --")
        self.subject_avg_label.setObjectName("statText")
        
        self.subject_status_label = QLabel("🎯 Estado: --")
        self.subject_status_label.setObjectName("statusText")
        
        self.subject_distribution_label = QLabel("📈 Distribución: --")
        self.subject_distribution_label.setObjectName("detailsText")
        self.subject_distribution_label.setWordWrap(True)
        
        performance_layout.addWidget(self.subject_avg_label)
        performance_layout.addWidget(self.subject_status_label)
        performance_layout.addWidget(self.subject_distribution_label)
        
        stats_layout.addWidget(subject_info_group)
        stats_layout.addWidget(performance_group)
        stats_layout.addStretch()
        
        content_splitter.addWidget(table_frame)
        content_splitter.addWidget(stats_frame)
        content_splitter.setSizes([700, 300])
        
        layout.addWidget(selection_frame)
        layout.addWidget(content_splitter)
        
        self.stats_tabs.addTab(subject_tab, "📚 Asignaturas")
    
    def create_ranking_tab(self):
        """Crear pestaña de ranking"""
        ranking_tab = QWidget()
        layout = QVBoxLayout(ranking_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header del ranking
        ranking_header = QFrame()
        ranking_header.setObjectName("rankingHeader")
        header_layout = QHBoxLayout(ranking_header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        header_title = QLabel("🏆 Ranking de Estudiantes")
        header_title.setObjectName("rankingTitle")
        
        self.ranking_count_label = QLabel("0 estudiantes clasificados")
        self.ranking_count_label.setObjectName("rankingCount")
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.ranking_count_label)
        
        # Tabla de ranking
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        self.ranking_table = QTableWidget()
        self.ranking_table.setColumnCount(5)
        self.ranking_table.setHorizontalHeaderLabels([
            "🏆 Posición", "👤 Estudiante", "📊 Promedio", "📚 Programa", "🎯 Estado"
        ])
        self.ranking_table.setObjectName("rankingTable")
        self.ranking_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ranking_table.verticalHeader().setVisible(False)
        self.ranking_table.setAlternatingRowColors(True)
        
        table_layout.addWidget(self.ranking_table)
        
        layout.addWidget(ranking_header)
        layout.addWidget(table_frame)
        
        self.stats_tabs.addTab(ranking_tab, "🏆 Ranking")
    
    def create_risk_tab(self):
        """Crear pestaña de estudiantes en riesgo"""
        risk_tab = QWidget()
        layout = QVBoxLayout(risk_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Configuración del umbral
        config_frame = QFrame()
        config_frame.setObjectName("configFrame")
        config_layout = QHBoxLayout(config_frame)
        config_layout.setContentsMargins(20, 15, 20, 15)
        
        threshold_label = QLabel("⚠️ Umbral de Riesgo:")
        threshold_label.setObjectName("configLabel")
        
        self.threshold_input = QDoubleSpinBox()
        self.threshold_input.setRange(1.0, 5.0)
        self.threshold_input.setSingleStep(0.1)
        self.threshold_input.setDecimals(2)
        self.threshold_input.setValue(3.0)
        self.threshold_input.setObjectName("thresholdInput")
        
        update_btn = QPushButton("🔄 Actualizar")
        update_btn.setObjectName("updateButton")
        update_btn.clicked.connect(self.update_risk_students)
        
        self.risk_count_label = QLabel("0 estudiantes en riesgo")
        self.risk_count_label.setObjectName("riskCount")
        
        config_layout.addWidget(threshold_label)
        config_layout.addWidget(self.threshold_input)
        config_layout.addWidget(update_btn)
        config_layout.addStretch()
        config_layout.addWidget(self.risk_count_label)
        
        # Tabla de estudiantes en riesgo
        table_frame = QFrame()
        table_frame.setObjectName("riskTableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        table_title = QLabel("⚠️ Estudiantes en Riesgo Académico")
        table_title.setObjectName("riskTitle")
        
        self.risk_students_table = QTableWidget()
        self.risk_students_table.setColumnCount(4)
        self.risk_students_table.setHorizontalHeaderLabels([
            "👤 Estudiante", "📊 Promedio", "📚 Programa", "📝 Total Notas"
        ])
        self.risk_students_table.setObjectName("riskTable")
        self.risk_students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.risk_students_table.verticalHeader().setVisible(False)
        self.risk_students_table.setAlternatingRowColors(True)
        
        table_layout.addWidget(table_title)
        table_layout.addWidget(self.risk_students_table)
        
        layout.addWidget(config_frame)
        layout.addWidget(table_frame)
        
        self.stats_tabs.addTab(risk_tab, "⚠️ En Riesgo")
    
    def create_visual_analysis_tab(self):
        """Crear pestaña de análisis visual"""
        visual_tab = QWidget()
        layout = QVBoxLayout(visual_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        visual_header = QFrame()
        visual_header.setObjectName("visualHeader")
        header_layout = QHBoxLayout(visual_header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        header_title = QLabel("📈 Análisis Visual de Datos")
        header_title.setObjectName("visualTitle")
        
        refresh_charts_btn = QPushButton("🔄 Actualizar Gráficos")
        refresh_charts_btn.setObjectName("refreshButton")
        refresh_charts_btn.clicked.connect(self.update_visual_analysis)
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_charts_btn)
        
        # Contenedor de gráficos
        charts_frame = QFrame()
        charts_frame.setObjectName("chartsFrame")
        charts_layout = QGridLayout(charts_frame)
        charts_layout.setSpacing(15)
        
        # Gráfico de distribución de calificaciones
        self.create_grade_distribution_chart(charts_layout, 0, 0)
        
        # Gráfico de rendimiento por programa
        self.create_program_performance_chart(charts_layout, 0, 1)
        
        # Gráfico de tendencias
        self.create_trends_chart(charts_layout, 1, 0, 1, 2)
        
        layout.addWidget(visual_header)
        layout.addWidget(charts_frame)
        
        self.stats_tabs.addTab(visual_tab, "📈 Análisis Visual")
    
    def create_grade_distribution_chart(self, parent_layout, row, col):
        """Crear gráfico de distribución de calificaciones"""
        chart_frame = QFrame()
        chart_frame.setObjectName("chartFrame")
        chart_frame.setFixedSize(400, 300)
        chart_layout = QVBoxLayout(chart_frame)
        
        chart_title = QLabel("📊 Distribución de Calificaciones")
        chart_title.setObjectName("chartTitle")
        chart_title.setAlignment(Qt.AlignCenter)
        
        self.grade_dist_figure = plt.figure(figsize=(5, 3), dpi=80)
        self.grade_dist_canvas = FigureCanvas(self.grade_dist_figure)
        self.grade_dist_canvas.setFixedSize(380, 250)
        
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.grade_dist_canvas)
        
        parent_layout.addWidget(chart_frame, row, col)
    
    def create_program_performance_chart(self, parent_layout, row, col):
        """Crear gráfico de rendimiento por programa"""
        chart_frame = QFrame()
        chart_frame.setObjectName("chartFrame")
        chart_frame.setFixedSize(400, 300)
        chart_layout = QVBoxLayout(chart_frame)
        
        chart_title = QLabel("📚 Rendimiento por Programa")
        chart_title.setObjectName("chartTitle")
        chart_title.setAlignment(Qt.AlignCenter)
        
        self.program_perf_figure = plt.figure(figsize=(5, 3), dpi=80)
        self.program_perf_canvas = FigureCanvas(self.program_perf_figure)
        self.program_perf_canvas.setFixedSize(380, 250)
        
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.program_perf_canvas)
        
        parent_layout.addWidget(chart_frame, row, col)
    
    def create_trends_chart(self, parent_layout, row, col, rowspan, colspan):
        """Crear gráfico de tendencias"""
        chart_frame = QFrame()
        chart_frame.setObjectName("chartFrame")
        chart_frame.setFixedHeight(300)
        chart_layout = QVBoxLayout(chart_frame)
        
        chart_title = QLabel("📈 Tendencias Académicas")
        chart_title.setObjectName("chartTitle")
        chart_title.setAlignment(Qt.AlignCenter)
        
        self.trends_figure = plt.figure(figsize=(10, 3), dpi=80)
        self.trends_canvas = FigureCanvas(self.trends_figure)
        self.trends_canvas.setFixedHeight(250)
        
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.trends_canvas)
        
        parent_layout.addWidget(chart_frame, row, col, rowspan, colspan)
    
    def create_action_section(self, parent_layout):
        """Crear sección de acciones"""
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botones de acción
        refresh_all_btn = QPushButton("🔄 Actualizar Todo")
        refresh_all_btn.setObjectName("primaryButton")
        refresh_all_btn.clicked.connect(self.update_all_data)
        
        export_stats_btn = QPushButton("📤 Exportar Estadísticas")
        export_stats_btn.setObjectName("secondaryButton")
        export_stats_btn.clicked.connect(self.export_statistics)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("🏠 Dashboard")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.parent.show_dashboard)
        
        action_layout.addWidget(refresh_all_btn)
        action_layout.addWidget(export_stats_btn)
        action_layout.addStretch()
        action_layout.addWidget(back_btn)
        
        parent_layout.addWidget(action_frame)
    
    def apply_modern_styles(self):
        """Aplicar estilos modernos con texto en negro y mejor organización"""
        self.setStyleSheet("""
            /* Frame principal */
            QWidget {
                background-color: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #000000;  /* Texto negro por defecto */
            }
            
            /* Header */
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
            }
            
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
            }
            
            #updateLabel {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.8);
            }
            
            /* Tarjetas de estadísticas */
            #statCard {
                background: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                min-height: 80px;
                border: 1px solid #e0e0e0;
            }
            
            #statCard QLabel {
                color: #000000;  /* Texto negro */
            }
            
            #cardValue {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;  /* Azul oscuro para valores */
            }
            
            /* Pestañas */
            #statsTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                background-color: white;
                margin-top: -2px;
            }
            
            #statsTabWidget QTabBar::tab {
                background: #f8f9fa;
                color: #000000;  /* Texto negro */
                padding: 12px 20px;
                margin: 2px;
                border: 1px solid #e0e0e0;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }
            
            #statsTabWidget QTabBar::tab:selected {
                background: white;
                color: #2c3e50;  /* Azul oscuro */
                border: 1px solid #e0e0e0;
                border-bottom: none;
            }
            
            /* Frames de sección */
            #selectionFrame, #configFrame, #actionFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }
            
            #rankingHeader, #visualHeader {
                background: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
            
            #riskTableFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }
            
            /* Labels */
            #selectionLabel, #configLabel {
                font-weight: bold;
                color: #000000;  /* Texto negro */
                font-size: 14px;
            }
            
            #sectionTitle, #rankingTitle, #visualTitle, #riskTitle {
                font-size: 16px;
                font-weight: bold;
                color: #000000;  /* Texto negro */
                margin-bottom: 10px;
            }
            
            #rankingCount, #riskCount {
                font-size: 14px;
                color: #000000;  /* Texto negro */
                font-weight: 500;
            }
            
            #infoText, #statText, #detailsText {
                color: #000000;  /* Texto negro */
                font-size: 13px;
                line-height: 1.4;
                margin: 5px 0;
            }
            
            #statusText {
                font-weight: bold;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 6px;
                margin: 5px 0;
                color: #000000;  /* Texto negro */
            }
            
            /* Tablas */
            #modernTable, #rankingTable, #riskTable {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            
            #modernTable::item, #rankingTable::item, #riskTable::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
                color: #000000;  /* Texto negro */
            }
            
            #modernTable::item:selected, #rankingTable::item:selected, #riskTable::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            /* Combos y inputs */
            #modernCombo, #thresholdInput, #searchInput {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: #000000;  /* Texto negro */
            }
            
            #modernCombo:focus, #thresholdInput:focus, #searchInput:focus {
                border-color: #667eea;
            }
            
            /* Grupos */
            #infoGroup {
                font-weight: bold;
                color: #000000;  /* Texto negro */
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin: 5px;
                background-color: white;
            }
            
            /* Frames de información */
            #tableFrame, #infoFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }
            
            /* Barra de progreso */
            #progressBar {
                height: 20px;
                border-radius: 10px;
                background-color: #f0f0f0;
                margin: 5px 0;
            }
            
            #progressBar::chunk {
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28a745, stop:0.5 #ffc107, stop:1 #dc3545);
            }
            
            /* Gráficos */
            #chartsFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
            }
            
            #chartFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
            
            #chartTitle {
                font-size: 14px;
                font-weight: bold;
                color: #000000;  /* Texto negro */
                margin-bottom: 5px;
            }
            
            /* Botones */
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
            
            #secondaryButton, #updateButton, #refreshButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #secondaryButton:hover, #updateButton:hover, #refreshButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
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
    
    def darken_color(self, hex_color, percent=15):
        """Oscurecer un color hexadecimal"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def update_all_data(self):
        """Actualizar todos los datos"""
        self.update_header_stats()
        self.update_student_combo()
        self.update_subject_combo()
        self.update_ranking()
        self.update_risk_students()
        self.update_visual_analysis()
        
        # Actualizar timestamp
        from datetime import datetime
        self.last_update_label.setText(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")
        
        # Mostrar mensaje
        if self.parent:
            self.parent.statusBar().showMessage("📊 Estadísticas actualizadas correctamente", 3000)
    
    def update_header_stats(self):
        """Actualizar estadísticas del header"""
        total_students = len(self.sistema.estudiantes)
        total_subjects = len(self.sistema.asignaturas)
        total_grades = len(self.sistema.notas_heap)
        
        # Calcular promedio del sistema
        if self.sistema.notas_heap:
            system_avg = sum(nota.calificacion for nota in self.sistema.notas_heap) / len(self.sistema.notas_heap)
        else:
            system_avg = 0.0
        
        # Actualizar cards
        self.total_students_card.value_label.setText(str(total_students))
        self.total_subjects_card.value_label.setText(str(total_subjects))
        self.total_grades_card.value_label.setText(str(total_grades))
        self.system_avg_card.value_label.setText(f"{system_avg:.2f}")
    
    def update_student_combo(self):
        """Actualizar combo de estudiantes"""
        current_text = self.student_combo.currentText()
        self.student_combo.clear()
        
        estudiantes = sorted(self.sistema.obtener_estudiantes(), key=lambda x: x.nombre)
        for est in estudiantes:
            self.student_combo.addItem(f"{est.nombre} ({est.codigo})", est.codigo)
        
        # Restaurar selección si existe
        index = self.student_combo.findText(current_text)
        if index >= 0:
            self.student_combo.setCurrentIndex(index)
        elif estudiantes:
            self.update_student_stats()
    
    def update_subject_combo(self):
        """Actualizar combo de asignaturas"""
        current_text = self.subject_combo.currentText()
        self.subject_combo.clear()
        
        asignaturas = sorted(self.sistema.obtener_asignaturas(), key=lambda x: x.nombre)
        for asig in asignaturas:
            self.subject_combo.addItem(f"{asig.nombre} ({asig.codigo})", asig.codigo)
        
        # Restaurar selección si existe
        index = self.subject_combo.findText(current_text)
        if index >= 0:
            self.subject_combo.setCurrentIndex(index)
        elif asignaturas:
            self.update_subject_stats()
    
    def filter_students(self):
        """Filtrar estudiantes en el combo"""
        search_text = self.student_search.text().lower()
        
        # Guardar selección actual
        current_data = self.student_combo.currentData()
        
        # Limpiar y repoblar
        self.student_combo.clear()
        estudiantes = sorted(self.sistema.obtener_estudiantes(), key=lambda x: x.nombre)
        
        for est in estudiantes:
            if search_text in est.nombre.lower() or search_text in est.codigo.lower():
                self.student_combo.addItem(f"{est.nombre} ({est.codigo})", est.codigo)
        
        # Restaurar selección si aún existe
        for i in range(self.student_combo.count()):
            if self.student_combo.itemData(i) == current_data:
                self.student_combo.setCurrentIndex(i)
                break
    
    def update_student_stats(self):
        """Actualizar estadísticas del estudiante"""
        self.student_notes_table.setRowCount(0)
        
        codigo = self.student_combo.currentData()
        if not codigo:
            self.clear_student_info()
            return
        
        # Obtener información del estudiante
        estudiante = self.sistema.estudiantes.get(codigo)
        if not estudiante:
            self.clear_student_info()
            return
        
        # Actualizar información básica
        info_text = f"""
        🔢 <b>Código:</b> {estudiante.codigo}
        👤 <b>Nombre:</b> {estudiante.nombre}
        📚 <b>Programa:</b> {estudiante.programa}
        📧 <b>Email:</b> {estudiante.email}
        📱 <b>Teléfono:</b> {estudiante.telefono}
        """
        self.student_info_label.setText(info_text.strip())
        
        # Obtener notas del estudiante
        notas = self.sistema.obtener_notas_estudiante(codigo)
        
        if not notas:
            self.clear_student_stats()
            return
        
        # Mostrar notas en la tabla
        for nota in sorted(notas, key=lambda x: x.asignatura):
            row = self.student_notes_table.rowCount()
            self.student_notes_table.insertRow(row)
            
            # Obtener nombre de asignatura
            asignatura = self.sistema.asignaturas.get(nota.asignatura, None)
            nombre_asignatura = asignatura.nombre if asignatura else nota.asignatura
            
            # Determinar estado
            if nota.calificacion >= 4.5:
                estado = "🌟 Excelente"
                color = QColor(46, 204, 113)
            elif nota.calificacion >= 4.0:
                estado = "✅ Buena"
                color = QColor(52, 152, 219)
            elif nota.calificacion >= 3.0:
                estado = "⚠️ Regular"
                color = QColor(241, 196, 15)
            else:
                estado = "❌ Deficiente"
                color = QColor(231, 76, 60)
            
            # Crear items
            items = [
                QTableWidgetItem(nombre_asignatura),
                QTableWidgetItem(f"{nota.calificacion:.2f}"),
                QTableWidgetItem(f"{nota.peso:.1f}%"),
                QTableWidgetItem(nota.fecha.strftime('%d/%m/%Y')),
                QTableWidgetItem(estado)
            ]
            
            # Aplicar colores
            items[1].setForeground(QBrush(color))
            items[1].setFont(QFont("Arial", 10, QFont.Bold))
            items[4].setForeground(QBrush(color))
            items[4].setFont(QFont("Arial", 9, QFont.Bold))
            
            for col, item in enumerate(items):
                self.student_notes_table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        
        # Calcular y mostrar estadísticas
        promedio = self.sistema.calcular_promedio_estudiante(codigo)
        promedio_ponderado = self.sistema.calcular_promedio_ponderado_estudiante(codigo)
        
        self.student_avg_label.setText(f"📊 Promedio Simple: {promedio:.2f}")
        self.student_weighted_avg_label.setText(f"⚖️ Promedio Ponderado: {promedio_ponderado:.2f}")
        
        # Actualizar barra de progreso
        self.student_progress_bar.setValue(int(promedio_ponderado * 10))
        
        # Estado académico
        if promedio_ponderado >= 4.5:
            estado = "🌟 Excelente"
            color_style = "background-color: #28a745; color: white;"
        elif promedio_ponderado >= 4.0:
            estado = "✅ Bueno"
            color_style = "background-color: #007bff; color: white;"
        elif promedio_ponderado >= 3.0:
            estado = "⚠️ Regular"
            color_style = "background-color: #ffc107; color: black;"
        else:
            estado = "❌ En Riesgo"
            color_style = "background-color: #dc3545; color: white;"
        
        self.student_status_label.setText(f"🎯 Estado: {estado}")
        self.student_status_label.setStyleSheet(f"padding: 8px; border-radius: 6px; {color_style}")
        
        # Estadísticas detalladas
        total_notas = len(notas)
        notas_excelentes = len([n for n in notas if n.calificacion >= 4.5])
        notas_buenas = len([n for n in notas if 4.0 <= n.calificacion < 4.5])
        notas_regulares = len([n for n in notas if 3.0 <= n.calificacion < 4.0])
        notas_deficientes = len([n for n in notas if n.calificacion < 3.0])
        
        details_text = f"""
        📊 <b>Total de calificaciones:</b> {total_notas}
        🌟 <b>Excelentes:</b> {notas_excelentes} ({(notas_excelentes/total_notas*100):.1f}%)
        ✅ <b>Buenas:</b> {notas_buenas} ({(notas_buenas/total_notas*100):.1f}%)
        ⚠️ <b>Regulares:</b> {notas_regulares} ({(notas_regulares/total_notas*100):.1f}%)
        ❌ <b>Deficientes:</b> {notas_deficientes} ({(notas_deficientes/total_notas*100):.1f}%)
        
        📈 <b>Tasa de éxito:</b> {((total_notas - notas_deficientes) / total_notas * 100):.1f}%
        """
        
        self.student_details_label.setText(details_text.strip())
    
    def clear_student_info(self):
        """Limpiar información del estudiante"""
        self.student_info_label.setText("Seleccione un estudiante")
        self.clear_student_stats()
    
    def clear_student_stats(self):
        """Limpiar estadísticas del estudiante"""
        self.student_avg_label.setText("📊 Promedio Simple: --")
        self.student_weighted_avg_label.setText("⚖️ Promedio Ponderado: --")
        self.student_status_label.setText("🎯 Estado: --")
        self.student_status_label.setStyleSheet("padding: 8px; border-radius: 6px; background-color: #6c757d; color: white;")
        self.student_progress_bar.setValue(0)
        self.student_details_label.setText("Sin datos disponibles")
    
    def update_subject_stats(self):
        """Actualizar estadísticas de la asignatura"""
        self.subject_notes_table.setRowCount(0)
        
        codigo = self.subject_combo.currentData()
        if not codigo:
            self.clear_subject_info()
            return
        
        # Obtener información de la asignatura
        asignatura = self.sistema.asignaturas.get(codigo)
        if not asignatura:
            self.clear_subject_info()
            return
        
        # Actualizar información básica
        profesor = self.sistema.profesores.get(asignatura.profesor, None)
        profesor_nombre = profesor.nombre if profesor else "No asignado"
        
        info_text = f"""
        🔢 <b>Código:</b> {asignatura.codigo}
        📚 <b>Nombre:</b> {asignatura.nombre}
        🎓 <b>Créditos:</b> {asignatura.creditos}
        👨‍🏫 <b>Profesor:</b> {profesor_nombre}
        """
        self.subject_info_label.setText(info_text.strip())
        
        # Obtener notas de la asignatura
        notas = self.sistema.obtener_notas_asignatura(codigo)
        
        if not notas:
            self.clear_subject_stats()
            return
        
        # Mostrar notas en la tabla
        for nota in sorted(notas, key=lambda x: x.estudiante):
            row = self.subject_notes_table.rowCount()
            self.subject_notes_table.insertRow(row)
            
            # Obtener nombre de estudiante
            estudiante = self.sistema.estudiantes.get(nota.estudiante, None)
            nombre_estudiante = estudiante.nombre if estudiante else nota.estudiante
            
            # Determinar estado
            if nota.calificacion >= 4.5:
                estado = "🌟 Excelente"
                color = QColor(46, 204, 113)
            elif nota.calificacion >= 4.0:
                estado = "✅ Buena"
                color = QColor(52, 152, 219)
            elif nota.calificacion >= 3.0:
                estado = "⚠️ Regular"
                color = QColor(241, 196, 15)
            else:
                estado = "❌ Deficiente"
                color = QColor(231, 76, 60)
            
            # Crear items
            items = [
                QTableWidgetItem(nombre_estudiante),
                QTableWidgetItem(f"{nota.calificacion:.2f}"),
                QTableWidgetItem(f"{nota.peso:.1f}%"),
                QTableWidgetItem(nota.fecha.strftime('%d/%m/%Y')),
                QTableWidgetItem(estado)
            ]
            
            # Aplicar colores
            items[1].setForeground(QBrush(color))
            items[1].setFont(QFont("Arial", 10, QFont.Bold))
            items[4].setForeground(QBrush(color))
            items[4].setFont(QFont("Arial", 9, QFont.Bold))
            
            for col, item in enumerate(items):
                self.subject_notes_table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        
        # Calcular estadísticas
        promedio = self.sistema.calcular_promedio_asignatura(codigo)
        self.subject_avg_label.setText(f"📊 Promedio: {promedio:.2f}")
        
        # Estado de la asignatura
        if promedio >= 4.5:
            estado = "🌟 Excelente desempeño"
            color_style = "background-color: #28a745; color: white;"
        elif promedio >= 4.0:
            estado = "✅ Buen desempeño"
            color_style = "background-color: #007bff; color: white;"
        elif promedio >= 3.0:
            estado = "⚠️ Desempeño regular"
            color_style = "background-color: #ffc107; color: black;"
        else:
            estado = "❌ Desempeño bajo"
            color_style = "background-color: #dc3545; color: white;"
        
        self.subject_status_label.setText(f"🎯 Estado: {estado}")
        self.subject_status_label.setStyleSheet(f"padding: 8px; border-radius: 6px; {color_style}")
        
        # Distribución de calificaciones
        total_notas = len(notas)
        excelentes = len([n for n in notas if n.calificacion >= 4.5])
        buenas = len([n for n in notas if 4.0 <= n.calificacion < 4.5])
        regulares = len([n for n in notas if 3.0 <= n.calificacion < 4.0])
        deficientes = len([n for n in notas if n.calificacion < 3.0])
        
        distribution_text = f"""
        📊 <b>Distribución de calificaciones:</b>
        🌟 Excelentes: {excelentes} ({(excelentes/total_notas*100):.1f}%)
        ✅ Buenas: {buenas} ({(buenas/total_notas*100):.1f}%)
        ⚠️ Regulares: {regulares} ({(regulares/total_notas*100):.1f}%)
        ❌ Deficientes: {deficientes} ({(deficientes/total_notas*100):.1f}%)
        
        📈 Tasa de aprobación: {((total_notas - deficientes) / total_notas * 100):.1f}%
        """
        
        self.subject_distribution_label.setText(distribution_text.strip())
    
    def clear_subject_info(self):
        """Limpiar información de la asignatura"""
        self.subject_info_label.setText("Seleccione una asignatura")
        self.clear_subject_stats()
    
    def clear_subject_stats(self):
        """Limpiar estadísticas de la asignatura"""
        self.subject_avg_label.setText("📊 Promedio: --")
        self.subject_status_label.setText("🎯 Estado: --")
        self.subject_status_label.setStyleSheet("padding: 8px; border-radius: 6px; background-color: #6c757d; color: white;")
        self.subject_distribution_label.setText("Sin datos disponibles")
    
    def update_ranking(self):
        """Actualizar ranking de estudiantes"""
        self.ranking_table.setRowCount(0)
        
        ranking = self.sistema.ranking_estudiantes()
        
        if not ranking:
            self.ranking_count_label.setText("0 estudiantes clasificados")
            return
        
        self.ranking_count_label.setText(f"{len(ranking)} estudiantes clasificados")
        
        for i, (codigo, promedio) in enumerate(ranking, 1):
            row = self.ranking_table.rowCount()
            self.ranking_table.insertRow(row)
            
            # Obtener información del estudiante
            estudiante = self.sistema.estudiantes.get(codigo, None)
            nombre_estudiante = estudiante.nombre if estudiante else codigo
            programa = estudiante.programa if estudiante else "Desconocido"
            
            # Determinar estado y medalla
            if i == 1:
                posicion = "🥇 1°"
                posicion_color = QColor(255, 215, 0)  # Oro
            elif i == 2:
                posicion = "🥈 2°"
                posicion_color = QColor(192, 192, 192)  # Plata
            elif i == 3:
                posicion = "🥉 3°"
                posicion_color = QColor(205, 127, 50)  # Bronce
            else:
                posicion = f"#{i}"
                posicion_color = QColor(108, 117, 125)  # Gris
            
            # Determinar estado académico
            if promedio >= 4.5:
                estado = "🌟 Excelente"
                estado_color = QColor(46, 204, 113)
            elif promedio >= 4.0:
                estado = "✅ Bueno"
                estado_color = QColor(52, 152, 219)
            elif promedio >= 3.0:
                estado = "⚠️ Regular"
                estado_color = QColor(241, 196, 15)
            else:
                estado = "❌ En Riesgo"
                estado_color = QColor(231, 76, 60)
            
            # Crear items
            items = [
                QTableWidgetItem(posicion),
                QTableWidgetItem(nombre_estudiante),
                QTableWidgetItem(f"{promedio:.2f}"),
                QTableWidgetItem(programa),
                QTableWidgetItem(estado)
            ]
            
            # Aplicar colores y formato
            items[0].setForeground(QBrush(posicion_color))
            items[0].setFont(QFont("Arial", 11, QFont.Bold))
            
            items[2].setForeground(QBrush(estado_color))
            items[2].setFont(QFont("Arial", 10, QFont.Bold))
            
            items[4].setForeground(QBrush(estado_color))
            items[4].setFont(QFont("Arial", 9, QFont.Bold))
            
            for col, item in enumerate(items):
                self.ranking_table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def update_risk_students(self):
        """Actualizar estudiantes en riesgo"""
        self.risk_students_table.setRowCount(0)
        
        umbral = self.threshold_input.value()
        estudiantes_riesgo = self.sistema.estudiantes_en_riesgo(umbral)
        
        if not estudiantes_riesgo:
            self.risk_count_label.setText("0 estudiantes en riesgo")
            return
        
        self.risk_count_label.setText(f"{len(estudiantes_riesgo)} estudiantes en riesgo")
        
        for codigo, promedio in estudiantes_riesgo:
            row = self.risk_students_table.rowCount()
            self.risk_students_table.insertRow(row)
            
            # Obtener información del estudiante
            estudiante = self.sistema.estudiantes.get(codigo, None)
            nombre_estudiante = estudiante.nombre if estudiante else codigo
            programa = estudiante.programa if estudiante else "Desconocido"
            
            # Contar notas del estudiante
            notas_estudiante = [n for n in self.sistema.notas_heap if n.estudiante == codigo]
            total_notas = len(notas_estudiante)
            
            # Crear items
            items = [
                QTableWidgetItem(nombre_estudiante),
                QTableWidgetItem(f"{promedio:.2f}"),
                QTableWidgetItem(programa),
                QTableWidgetItem(str(total_notas))
            ]
            
            # Aplicar color rojo al promedio
            items[1].setForeground(QBrush(QColor(231, 76, 60)))
            items[1].setFont(QFont("Arial", 10, QFont.Bold))
            
            for col, item in enumerate(items):
                self.risk_students_table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def update_visual_analysis(self):
        """Actualizar análisis visual"""
        self.update_grade_distribution_chart()
        self.update_program_performance_chart()
        self.update_trends_chart()
    
    def update_grade_distribution_chart(self):
        """Actualizar gráfico de distribución de calificaciones"""
        self.grade_dist_figure.clear()
        ax = self.grade_dist_figure.add_subplot(111)
        
        if not self.sistema.notas_heap:
            ax.text(0.5, 0.5, 'Sin datos disponibles', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, color='gray')
            self.grade_dist_canvas.draw()
            return
        
        # Obtener calificaciones
        calificaciones = [nota.calificacion for nota in self.sistema.notas_heap]
        
        # Crear histograma
        colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
        n, bins, patches = ax.hist(calificaciones, bins=10, edgecolor='white', linewidth=1.5)
        
        # Aplicar colores
        for i, patch in enumerate(patches):
            patch.set_facecolor(colors[i % len(colors)])
            patch.set_alpha(0.8)
        
        ax.set_title('Distribución de Calificaciones', fontweight='bold', fontsize=10)
        ax.set_xlabel('Calificación', fontsize=9)
        ax.set_ylabel('Cantidad', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        self.grade_dist_figure.tight_layout()
        self.grade_dist_canvas.draw()
    
    def update_program_performance_chart(self):
        """Actualizar gráfico de rendimiento por programa"""
        self.program_perf_figure.clear()
        ax = self.program_perf_figure.add_subplot(111)
        
        # Calcular promedio por programa
        programas_promedio = {}
        for estudiante in self.sistema.estudiantes.values():
            promedio = self.sistema.calcular_promedio_estudiante(estudiante.codigo)
            if promedio > 0:
                if estudiante.programa not in programas_promedio:
                    programas_promedio[estudiante.programa] = []
                programas_promedio[estudiante.programa].append(promedio)
        
        if not programas_promedio:
            ax.text(0.5, 0.5, 'Sin datos disponibles', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, color='gray')
            self.program_perf_canvas.draw()
            return
        
        # Calcular promedios finales
        programas = list(programas_promedio.keys())
        promedios = [sum(programas_promedio[p]) / len(programas_promedio[p]) for p in programas]
        
        # Crear gráfico de barras
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        bars = ax.bar(programas, promedios, color=[colors[i % len(colors)] for i in range(len(programas))])
        
        # Agregar valores en las barras
        for bar, promedio in zip(bars, promedios):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   f'{promedio:.2f}', ha='center', va='bottom', fontsize=8)
        
        ax.set_title('Promedio por Programa', fontweight='bold', fontsize=10)
        ax.set_ylabel('Promedio', fontsize=9)
        ax.set_ylim(0, 5)
        ax.grid(True, alpha=0.3)
        
        # Rotar etiquetas si son muy largas
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
        
        self.program_perf_figure.tight_layout()
        self.program_perf_canvas.draw()
    
    def update_trends_chart(self):
        """Actualizar gráfico de tendencias"""
        self.trends_figure.clear()
        ax = self.trends_figure.add_subplot(111)
        
        if not self.sistema.notas_heap:
            ax.text(0.5, 0.5, 'Sin datos disponibles', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, color='gray')
            self.trends_canvas.draw()
            return
        
        # Agrupar notas por fecha
        from collections import defaultdict
        import datetime
        
        notas_por_fecha = defaultdict(list)
        for nota in self.sistema.notas_heap:
            fecha_str = nota.fecha.strftime('%Y-%m')
            notas_por_fecha[fecha_str].append(nota.calificacion)
        
        if len(notas_por_fecha) < 2:
            ax.text(0.5, 0.5, 'Datos insuficientes para mostrar tendencias', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, color='gray')
            self.trends_canvas.draw()
            return
        
        # Calcular promedios por mes
        fechas = sorted(notas_por_fecha.keys())
        promedios = [sum(notas_por_fecha[fecha]) / len(notas_por_fecha[fecha]) for fecha in fechas]
        
        # Crear gráfico de línea
        ax.plot(fechas, promedios, marker='o', linewidth=2, markersize=6, color='#3498db')
        ax.fill_between(fechas, promedios, alpha=0.3, color='#3498db')
        
        ax.set_title('Tendencia de Calificaciones por Mes', fontweight='bold', fontsize=10)
        ax.set_ylabel('Promedio', fontsize=9)
        ax.set_ylim(0, 5)
        ax.grid(True, alpha=0.3)
        
        # Rotar etiquetas de fecha
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
        
        self.trends_figure.tight_layout()
        self.trends_canvas.draw()
    
    def export_statistics(self):
        """Exportar estadísticas a archivo"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "📤 Exportar Estadísticas", 
            "estadisticas_academicas.txt", 
            "Archivos de texto (*.txt);;Todos los archivos (*)", 
            options=options
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write("📊 REPORTE DE ESTADÍSTICAS ACADÉMICAS\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Estadísticas generales
                    f.write("📈 ESTADÍSTICAS GENERALES\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"👥 Total de estudiantes: {len(self.sistema.estudiantes)}\n")
                    f.write(f"📚 Total de asignaturas: {len(self.sistema.asignaturas)}\n")
                    f.write(f"📝 Total de calificaciones: {len(self.sistema.notas_heap)}\n")
                    
                    if self.sistema.notas_heap:
                        promedio_sistema = sum(n.calificacion for n in self.sistema.notas_heap) / len(self.sistema.notas_heap)
                        f.write(f"📊 Promedio del sistema: {promedio_sistema:.2f}\n\n")
                    
                    # Ranking de estudiantes
                    f.write("🏆 RANKING DE ESTUDIANTES\n")
                    f.write("-" * 30 + "\n")
                    ranking = self.sistema.ranking_estudiantes()
                    for i, (codigo, promedio) in enumerate(ranking[:10], 1):
                        estudiante = self.sistema.estudiantes.get(codigo)
                        nombre = estudiante.nombre if estudiante else codigo
                        f.write(f"{i:2d}. {nombre}: {promedio:.2f}\n")
                    
                    # Estudiantes en riesgo
                    f.write(f"\n⚠️ ESTUDIANTES EN RIESGO (< {self.threshold_input.value()})\n")
                    f.write("-" * 30 + "\n")
                    estudiantes_riesgo = self.sistema.estudiantes_en_riesgo(self.threshold_input.value())
                    for codigo, promedio in estudiantes_riesgo:
                        estudiante = self.sistema.estudiantes.get(codigo)
                        nombre = estudiante.nombre if estudiante else codigo
                        f.write(f"• {nombre}: {promedio:.2f}\n")
                    
                    f.write(f"\nReporte generado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                
                QMessageBox.information(self, "✅ Exportación Exitosa", 
                                      f"Las estadísticas se exportaron correctamente a:\n{file_name}")
                
            except Exception as e:
                QMessageBox.warning(self, "❌ Error de Exportación", 
                                  f"No se pudieron exportar las estadísticas:\n{str(e)}")