from PyQt5.QtWidgets import (QMainWindow, QStackedWidget, QTabWidget, QToolBar, 
                            QAction, QMessageBox, QMenuBar, QMenu, QStatusBar, QDialog,
                            QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame)
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QLinearGradient, QPainter
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from models.sistema_notas import SistemaNotas
from .dashboard import DashboardWindow
from .tabs.estudiantes import StudentsTab
from .tabs.asignaturas import SubjectsTab
from .tabs.notas import NotesTab
from .tabs.estadisticas import StatsTab
from .tabs.profesores import ProfesoresTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaNotas()
        self.setWindowTitle("🎓 Sistema de Gestión Académica - Versión Profesional")
        self.setGeometry(100, 100, 1400, 900)  # Ventana más grande
        self.setMinimumSize(1200, 800)
        
        self.setup_ui()
        self.setup_modern_theme()
        self.create_modern_menu_bar()
        self.create_modern_toolbar()
        self.setup_status_bar()
        
        # Mensaje de bienvenida mejorado
        self.statusBar().showMessage("✅ Sistema listo - Bienvenido al Sistema de Gestión Académica")
    
    def setup_ui(self):
        # Configurar ventana principal con stacked widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Crear dashboard
        self.dashboard = DashboardWindow(self.sistema, self)
        self.dashboard.add_student_btn.clicked.connect(self.show_add_student_dialog)
        self.dashboard.add_subject_btn.clicked.connect(self.show_add_subject_dialog)
        self.dashboard.add_profesor_btn.clicked.connect(self.show_add_profesor_dialog)
        self.dashboard.add_note_btn.clicked.connect(self.show_add_note_dialog)
        self.dashboard.view_all_btn.clicked.connect(self.show_main_tabs)
        
        # Crear ventana principal con pestañas mejoradas
        self.main_tabs = QTabWidget()
        self.main_tabs.setTabPosition(QTabWidget.North)
        self.main_tabs.setMovable(True)  # Pestañas movibles
        self.main_tabs.setTabsClosable(False)
        
        # Crear pestañas con iconos mejorados
        self.students_tab = StudentsTab(self.sistema, self)
        self.subjects_tab = SubjectsTab(self.sistema, self)
        self.profesores_tab = ProfesoresTab(self.sistema, self)
        self.notes_tab = NotesTab(self.sistema, self)
        self.stats_tab = StatsTab(self.sistema, self)
        
        # Agregar pestañas con iconos y tooltips
        self.main_tabs.addTab(self.students_tab, "👥 Estudiantes")
        self.main_tabs.addTab(self.subjects_tab, "📚 Asignaturas")
        self.main_tabs.addTab(self.profesores_tab, "👨‍🏫 Profesores")
        self.main_tabs.addTab(self.notes_tab, "📝 Notas")
        self.main_tabs.addTab(self.stats_tab, "📊 Estadísticas")
        
        # Configurar tooltips para las pestañas
        self.main_tabs.setTabToolTip(0, "Gestionar información de estudiantes")
        self.main_tabs.setTabToolTip(1, "Administrar asignaturas y materias")
        self.main_tabs.setTabToolTip(2, "Gestionar profesores y docentes")
        self.main_tabs.setTabToolTip(3, "Registrar y consultar calificaciones")
        self.main_tabs.setTabToolTip(4, "Ver reportes y estadísticas del sistema")
        
        # Agregar widgets al stacked widget
        self.central_widget.addWidget(self.dashboard)
        self.central_widget.addWidget(self.main_tabs)
        
        # Mostrar dashboard primero
        self.central_widget.setCurrentIndex(0)
    
    def setup_modern_theme(self):
        """Configura un tema moderno y profesional"""
        self.setStyleSheet("""
            /* Estilo general de la ventana principal */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #2c3e50;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            /* Barra de menú moderna */
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QMenuBar::item {
                background: transparent;
                padding: 8px 16px;
                border-radius: 6px;
                margin: 2px;
            }
            
            QMenuBar::item:selected {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 6px;
            }
            
            QMenuBar::item:pressed {
                background: rgba(255, 255, 255, 0.3);
            }
            
            /* Menús desplegables */
            QMenu {
                background-color: #ffffff;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 8px;
                color: #2c3e50;
                font-size: 13px;
            }
            
            QMenu::item {
                background-color: transparent;
                padding: 8px 20px;
                border-radius: 6px;
                margin: 2px;
            }
            
            QMenu::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            QMenu::separator {
                height: 1px;
                background: #dee2e6;
                margin: 5px 10px;
            }
            
            /* Barra de herramientas moderna */
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: none;
                border-bottom: 2px solid #e9ecef;
                padding: 8px;
                spacing: 4px;
            }
            
            QToolBar::separator {
                background: #dee2e6;
                width: 2px;
                margin: 4px 8px;
                border-radius: 1px;
            }
            
            /* Botones de la barra de herramientas */
            QToolBar QToolButton {
                background: transparent;
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
                font-weight: bold;
                color: #495057;
            }
            
            QToolBar QToolButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: 2px solid #5a67d8;
            }
            
            QToolBar QToolButton:pressed {
                background: #4c51bf;
                color: white;
            }
            
            /* Pestañas modernas */
            QTabWidget::pane {
                border: 2px solid #e9ecef;
                border-radius: 10px;
                background-color: #ffffff;
                margin-top: -2px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #495057;
                padding: 12px 20px;
                margin: 2px;
                border: 2px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: 2px solid #5a67d8;
                border-bottom: none;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e3f2fd, stop:1 #bbdefb);
                color: #1976d2;
            }
            
            /* Barra de estado moderna */
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-top: 2px solid #dee2e6;
                color: #495057;
                font-weight: 500;
                padding: 4px;
            }
            
            /* Tooltips mejorados */
            QToolTip {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #34495e;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            
            /* Scrollbars personalizados */
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background-color: #6c757d;
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #495057;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
    
    def create_modern_menu_bar(self):
        """Crea una barra de menú moderna y organizada"""
        menu_bar = self.menuBar()
        
        # Menú Archivo con iconos
        file_menu = menu_bar.addMenu("📁 Archivo")
        
        dashboard_action = QAction("🏠 Dashboard", self)
        dashboard_action.setShortcut("Ctrl+H")
        dashboard_action.setStatusTip("Volver al panel principal")
        dashboard_action.triggered.connect(self.show_dashboard)
        file_menu.addAction(dashboard_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("📤 Exportar Datos", self)
        export_action.setShortcut("Ctrl+E")
        export_action.setStatusTip("Exportar datos a archivo CSV")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        import_action = QAction("📥 Importar Datos", self)
        import_action.setShortcut("Ctrl+I")
        import_action.setStatusTip("Importar datos desde archivo CSV")
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Cerrar la aplicación")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Gestión (antes Editar)
        manage_menu = menu_bar.addMenu("⚙️ Gestión")
        
        add_student_action = QAction("👤 Nuevo Estudiante", self)
        add_student_action.setShortcut("Ctrl+1")
        add_student_action.setStatusTip("Registrar un nuevo estudiante")
        add_student_action.triggered.connect(self.show_add_student_dialog)
        manage_menu.addAction(add_student_action)
        
        add_subject_action = QAction("📖 Nueva Asignatura", self)
        add_subject_action.setShortcut("Ctrl+2")
        add_subject_action.setStatusTip("Crear una nueva asignatura")
        add_subject_action.triggered.connect(self.show_add_subject_dialog)
        manage_menu.addAction(add_subject_action)
        
        add_profesor_action = QAction("👨‍🏫 Nuevo Profesor", self)
        add_profesor_action.setShortcut("Ctrl+3")
        add_profesor_action.setStatusTip("Registrar un nuevo profesor")
        add_profesor_action.triggered.connect(self.show_add_profesor_dialog)
        manage_menu.addAction(add_profesor_action)
        
        manage_menu.addSeparator()
        
        add_note_action = QAction("📝 Nueva Calificación", self)
        add_note_action.setShortcut("Ctrl+N")
        add_note_action.setStatusTip("Registrar una nueva calificación")
        add_note_action.triggered.connect(self.show_add_note_dialog)
        manage_menu.addAction(add_note_action)
        
        # Menú Navegación (antes Ver)
        nav_menu = menu_bar.addMenu("🧭 Navegación")
        
        view_students_action = QAction("👥 Ver Estudiantes", self)
        view_students_action.setShortcut("F1")
        view_students_action.setStatusTip("Ir a la sección de estudiantes")
        view_students_action.triggered.connect(lambda: self.show_main_tab(0))
        nav_menu.addAction(view_students_action)
        
        view_subjects_action = QAction("📚 Ver Asignaturas", self)
        view_subjects_action.setShortcut("F2")
        view_subjects_action.setStatusTip("Ir a la sección de asignaturas")
        view_subjects_action.triggered.connect(lambda: self.show_main_tab(1))
        nav_menu.addAction(view_subjects_action)
        
        view_profesor_action = QAction("👨‍🏫 Ver Profesores", self)
        view_profesor_action.setShortcut("F3")
        view_profesor_action.setStatusTip("Ir a la sección de profesores")
        view_profesor_action.triggered.connect(lambda: self.show_main_tab(2))
        nav_menu.addAction(view_profesor_action)
        
        view_notes_action = QAction("📝 Ver Calificaciones", self)
        view_notes_action.setShortcut("F4")
        view_notes_action.setStatusTip("Ir a la sección de calificaciones")
        view_notes_action.triggered.connect(lambda: self.show_main_tab(3))
        nav_menu.addAction(view_notes_action)
        
        view_stats_action = QAction("📊 Ver Estadísticas", self)
        view_stats_action.setShortcut("F5")
        view_stats_action.setStatusTip("Ir a la sección de estadísticas")
        view_stats_action.triggered.connect(lambda: self.show_main_tab(4))
        nav_menu.addAction(view_stats_action)
        
        # Menú Ayuda
        help_menu = menu_bar.addMenu("❓ Ayuda")
        
        about_action = QAction("ℹ️ Acerca de", self)
        about_action.setStatusTip("Información sobre la aplicación")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction("⌨️ Atajos de Teclado", self)
        shortcuts_action.setStatusTip("Ver lista de atajos de teclado")
        shortcuts_action.triggered.connect(self.show_shortcuts_dialog)
        help_menu.addAction(shortcuts_action)
    
    def create_modern_toolbar(self):
        """Crea una barra de herramientas moderna y funcional"""
        toolbar = QToolBar("Herramientas Principales")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)
        
        # Sección de Navegación
        dashboard_action = QAction(QIcon.fromTheme("go-home"), "Dashboard", self)
        dashboard_action.setStatusTip("Volver al panel principal (Ctrl+H)")
        dashboard_action.triggered.connect(self.show_dashboard)
        toolbar.addAction(dashboard_action)
        
        toolbar.addSeparator()
        
        # Sección de Gestión
        add_student_action = QAction(QIcon.fromTheme("list-add-user"), "Estudiante", self)
        add_student_action.setStatusTip("Agregar nuevo estudiante (Ctrl+1)")
        add_student_action.triggered.connect(self.show_add_student_dialog)
        toolbar.addAction(add_student_action)
        
        add_subject_action = QAction(QIcon.fromTheme("list-add"), "Asignatura", self)
        add_subject_action.setStatusTip("Agregar nueva asignatura (Ctrl+2)")
        add_subject_action.triggered.connect(self.show_add_subject_dialog)
        toolbar.addAction(add_subject_action)
        
        add_profesor_action = QAction(QIcon.fromTheme("list-add-user"), "Profesor", self)
        add_profesor_action.setStatusTip("Agregar nuevo profesor (Ctrl+3)")
        add_profesor_action.triggered.connect(self.show_add_profesor_dialog)
        toolbar.addAction(add_profesor_action)
        
        add_note_action = QAction(QIcon.fromTheme("list-add-document"), "Calificación", self)
        add_note_action.setStatusTip("Agregar nueva calificación (Ctrl+N)")
        add_note_action.triggered.connect(self.show_add_note_dialog)
        toolbar.addAction(add_note_action)
        
        toolbar.addSeparator()
        
        # Sección de Datos
        export_action = QAction(QIcon.fromTheme("document-export"), "Exportar", self)
        export_action.setStatusTip("Exportar datos a CSV (Ctrl+E)")
        export_action.triggered.connect(self.export_data)
        toolbar.addAction(export_action)
        
        import_action = QAction(QIcon.fromTheme("document-import"), "Importar", self)
        import_action.setStatusTip("Importar datos desde CSV (Ctrl+I)")
        import_action.triggered.connect(self.import_data)
        toolbar.addAction(import_action)
    
    def setup_status_bar(self):
        """Configura una barra de estado informativa"""
        status_bar = self.statusBar()
        status_bar.setFixedHeight(30)
        
        # Etiqueta para mostrar información del sistema
        self.system_info_label = QLabel()
        self.update_system_info()
        status_bar.addPermanentWidget(self.system_info_label)
    
    def update_system_info(self):
        """Actualiza la información del sistema en la barra de estado"""
        total_estudiantes = len(self.sistema.estudiantes)
        total_asignaturas = len(self.sistema.asignaturas)
        total_profesores = len(self.sistema.profesores)
        total_notas = len(self.sistema.notas_heap)
        
        info_text = f"👥 {total_estudiantes} estudiantes | 📚 {total_asignaturas} asignaturas | 👨‍🏫 {total_profesores} profesores | 📝 {total_notas} calificaciones"
        self.system_info_label.setText(info_text)
    
    def show_about_dialog(self):
        """Muestra el diálogo Acerca de"""
        QMessageBox.about(self, "Acerca del Sistema", 
                         """
                         <h2>🎓 Sistema de Gestión Académica</h2>
                         <p><b>Versión:</b> 2.0 Profesional</p>
                         <p><b>Desarrollado con:</b> Python & PyQt5</p>
                         <p><b>Características:</b></p>
                         <ul>
                         <li>Gestión completa de estudiantes</li>
                         <li>Administración de asignaturas</li>
                         <li>Control de profesores</li>
                         <li>Registro de calificaciones</li>
                         <li>Estadísticas avanzadas</li>
                         <li>Importación/Exportación CSV</li>
                         </ul>
                         <p><i>Sistema diseñado para instituciones educativas</i></p>
                         """)
    
    def show_shortcuts_dialog(self):
        """Muestra el diálogo de atajos de teclado"""
        QMessageBox.information(self, "Atajos de Teclado", 
                               """
                               <h3>⌨️ Atajos de Teclado Disponibles</h3>
                               <table>
                               <tr><td><b>Ctrl+H</b></td><td>Ir al Dashboard</td></tr>
                               <tr><td><b>Ctrl+1</b></td><td>Nuevo Estudiante</td></tr>
                               <tr><td><b>Ctrl+2</b></td><td>Nueva Asignatura</td></tr>
                               <tr><td><b>Ctrl+3</b></td><td>Nuevo Profesor</td></tr>
                               <tr><td><b>Ctrl+N</b></td><td>Nueva Calificación</td></tr>
                               <tr><td><b>Ctrl+E</b></td><td>Exportar Datos</td></tr>
                               <tr><td><b>Ctrl+I</b></td><td>Importar Datos</td></tr>
                               <tr><td><b>F1-F5</b></td><td>Navegar entre secciones</td></tr>
                               <tr><td><b>Ctrl+Q</b></td><td>Salir</td></tr>
                               </table>
                               """)
    
    # Métodos para mostrar diálogos (mantenidos igual pero con mensajes mejorados)
    def show_add_student_dialog(self):
        """Muestra el diálogo para agregar un nuevo estudiante"""
        from .dialogs.estudiante import StudentDialog
        dialog = StudentDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            from models.estudiante import Estudiante
            data = dialog.get_data()
            
            if not data['codigo'] or not data['nombre'] or not data['programa']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Los campos Código, Nombre y Programa son obligatorios.")
                return
                
            nuevo_estudiante = Estudiante(
                data['codigo'],
                data['nombre'],
                data['programa'],
                data['email'],
                data['telefono']
            )
            if self.sistema.agregar_estudiante(nuevo_estudiante):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Estudiante '{data['nombre']}' agregado correctamente.")
                self.students_tab.update_table()
                self.stats_tab.update_student_combo()
                self.dashboard.update_stats()
                self.update_system_info()
                self.show_main_tab(0)
                self.statusBar().showMessage(f"✅ Estudiante {data['nombre']} registrado", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  f"El código '{data['codigo']}' ya existe en el sistema.")
    
    def show_edit_student_dialog(self, estudiante):
        """Muestra el diálogo para editar un estudiante existente"""
        from .dialogs.estudiante import StudentDialog
        dialog = StudentDialog(estudiante, self)
        if dialog.exec_() == QDialog.Accepted:
            from models.estudiante import Estudiante
            data = dialog.get_data()
            
            if not data['codigo'] or not data['nombre'] or not data['programa']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Los campos Código, Nombre y Programa son obligatorios.")
                return
                
            nuevo_estudiante = Estudiante(
                data['codigo'],
                data['nombre'],
                data['programa'],
                data['email'],
                data['telefono']
            )
            if self.sistema.editar_estudiante(data['codigo'], nuevo_estudiante):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Estudiante '{data['nombre']}' actualizado correctamente.")
                self.students_tab.update_table()
                self.stats_tab.update_student_combo()
                self.dashboard.update_stats()
                self.update_system_info()
                self.statusBar().showMessage(f"✅ Estudiante {data['nombre']} actualizado", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", "No se pudo actualizar el estudiante.")
    
    def show_add_subject_dialog(self):
        """Muestra el diálogo para agregar una nueva asignatura"""
        from .dialogs.asignatura import SubjectDialog
        dialog = SubjectDialog(parent=self, sistema=self.sistema)
        if dialog.exec_() == QDialog.Accepted:
            from models.asignatura import Asignatura
            data = dialog.get_data()
            
            if not data['codigo'] or not data['nombre']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Los campos Código y Nombre son obligatorios.")
                return
                
            nueva_asignatura = Asignatura(
                data['codigo'],
                data['nombre'],
                data['creditos'],
                data['profesor']
            )
            if self.sistema.agregar_asignatura(nueva_asignatura):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Asignatura '{data['nombre']}' agregada correctamente.")
                self.subjects_tab.update_table()
                self.stats_tab.update_subject_combo()
                self.dashboard.update_stats()
                self.update_system_info()
                self.show_main_tab(1)
                self.statusBar().showMessage(f"✅ Asignatura {data['nombre']} registrada", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  f"El código '{data['codigo']}' ya existe en el sistema.")
    
    def show_edit_subject_dialog(self, asignatura):
        """Muestra el diálogo para editar una asignatura existente"""
        from .dialogs.asignatura import SubjectDialog
        dialog = SubjectDialog(sistema=self.sistema, parent=self, asignatura=asignatura)
        if dialog.exec_() == QDialog.Accepted:
            from models.asignatura import Asignatura
            data = dialog.get_data()
            
            if not data['codigo'] or not data['nombre']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Los campos Código y Nombre son obligatorios.")
                return
                
            nueva_asignatura = Asignatura(
                data['codigo'],
                data['nombre'],
                data['creditos'],
                data['profesor']
            )
            if self.sistema.editar_asignatura(data['codigo'], nueva_asignatura):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Asignatura '{data['nombre']}' actualizada correctamente.")
                self.subjects_tab.update_table()
                self.stats_tab.update_subject_combo()
                self.dashboard.update_stats()
                self.update_system_info()
                self.statusBar().showMessage(f"✅ Asignatura {data['nombre']} actualizada", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", "No se pudo actualizar la asignatura.")
    
    def show_add_profesor_dialog(self):
        """Muestra el diálogo para agregar un nuevo profesor"""
        from .dialogs.profesor import ProfesorDialog
        dialog = ProfesorDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            from models.profesor import Profesor
            data = dialog.get_data()
            
            if not data['id_profesor'] or not data['nombre']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Los campos ID y Nombre son obligatorios.")
                return
                
            nuevo_profesor = Profesor(
                data['id_profesor'],
                data['nombre'],
                data['email'],
                data['telefono'],
                data['especialidad']
            )
            
            if self.sistema.agregar_profesor(nuevo_profesor):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Profesor '{data['nombre']}' agregado correctamente.")
                self.profesores_tab.update_table()
                self.update_system_info()
                self.show_main_tab(2)
                self.statusBar().showMessage(f"✅ Profesor {data['nombre']} registrado", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  f"El ID '{data['id_profesor']}' ya existe en el sistema.")
    
    def show_add_note_dialog(self):
        """Muestra el diálogo para agregar una nueva nota"""
        if not self.sistema.estudiantes:
            QMessageBox.warning(self, "⚠️ Sin Estudiantes", 
                              "No hay estudiantes registrados.\nRegistre al menos un estudiante primero.")
            return
            
        if not self.sistema.asignaturas:
            QMessageBox.warning(self, "⚠️ Sin Asignaturas", 
                              "No hay asignaturas registradas.\nRegistre al menos una asignatura primero.")
            return
            
        from .dialogs.nota import NoteDialog
        dialog = NoteDialog(self.sistema, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            from models.nota import Nota
            data = dialog.get_data()
            
            if not data['estudiante'] or not data['asignatura']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Debe seleccionar un estudiante y una asignatura.")
                return
                
            nueva_nota = Nota(
                data['estudiante'],
                data['asignatura'],
                data['calificacion'],
                data['fecha'],
                data['peso'],
                data['descripcion']
            )
            
            if self.sistema.agregar_nota(nueva_nota):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Calificación {data['calificacion']} registrada correctamente.")
                self.notes_tab.update_table()
                self.dashboard.update_stats()
                self.update_system_info()
                self.show_main_tab(3)
                self.statusBar().showMessage(f"✅ Calificación {data['calificacion']} registrada", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", 
                                  "No se pudo agregar la calificación.\nVerifique estudiante y asignatura.")
    
    def show_edit_note_dialog(self, nota):
        """Muestra el diálogo para editar una nota existente"""
        from .dialogs.nota import NoteDialog
        dialog = NoteDialog(self.sistema, nota, self)
        if dialog.exec_() == QDialog.Accepted:
            from models.nota import Nota
            data = dialog.get_data()
            
            if not data['estudiante'] or not data['asignatura']:
                QMessageBox.warning(self, "⚠️ Campos Requeridos", 
                                  "Debe seleccionar un estudiante y una asignatura.")
                return
                
            nueva_nota = Nota(
                data['estudiante'],
                data['asignatura'],
                data['calificacion'],
                data['fecha'],
                data['peso'],
                data['descripcion']
            )
            
            indice = self.notes_tab.table.currentRow()
            if self.sistema.editar_nota(indice, nueva_nota):
                QMessageBox.information(self, "✅ Éxito", 
                                      f"Calificación actualizada a {data['calificacion']}.")
                self.notes_tab.update_table()
                self.dashboard.update_stats()
                self.update_system_info()
                self.statusBar().showMessage(f"✅ Calificación actualizada", 3000)
            else:
                QMessageBox.warning(self, "❌ Error", "No se pudo actualizar la calificación.")
    
    # Métodos de navegación mejorados
    def show_dashboard(self):
        """Muestra el dashboard principal"""
        self.central_widget.setCurrentIndex(0)
        self.dashboard.update_stats()
        self.statusBar().showMessage("📊 Mostrando Dashboard Principal", 2000)
    
    def show_main_tabs(self):
        """Muestra las pestañas principales"""
        self.central_widget.setCurrentIndex(1)
        self.main_tabs.setCurrentIndex(0)
        self.statusBar().showMessage("📋 Mostrando Gestión de Datos", 2000)
    
    def show_main_tab(self, index):
        """Muestra una pestaña específica"""
        self.central_widget.setCurrentIndex(1)
        self.main_tabs.setCurrentIndex(index)
        
        tab_names = ["Estudiantes", "Asignaturas", "Profesores", "Calificaciones", "Estadísticas"]
        if 0 <= index < len(tab_names):
            self.statusBar().showMessage(f"📋 Mostrando sección: {tab_names[index]}", 2000)
        
        # Actualizar la pestaña seleccionada
        if index == 0:
            self.students_tab.update_table()
        elif index == 1:
            self.subjects_tab.update_table()
        elif index == 2:
            self.profesores_tab.update_table()
        elif index == 3:
            self.notes_tab.update_table()
        elif index == 4:
            self.stats_tab.update_student_combo()
            self.stats_tab.update_subject_combo()
            self.stats_tab.update_ranking()
            self.stats_tab.update_risk_students()
    
    # Métodos de importación/exportación mejorados
    def export_data(self):
        """Exporta los datos del sistema"""
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "📤 Exportar Datos del Sistema", 
            "datos_academicos.csv", 
            "Archivos CSV (*.csv);;Todos los archivos (*)", 
            options=options
        )
        
        if file_name:
            if not file_name.endswith('.csv'):
                file_name += '.csv'
            
            success = self.sistema.exportar_csv(file_name)
            if success:
                QMessageBox.information(self, "✅ Exportación Exitosa", 
                                      f"Los datos se exportaron correctamente a:\n{file_name}")
                self.statusBar().showMessage(f"✅ Datos exportados a {file_name}", 5000)
            else:
                QMessageBox.warning(self, "❌ Error de Exportación", 
                                  "No se pudieron exportar los datos.\nVerifique los permisos del archivo.")
    
    def import_data(self):
        """Importa datos al sistema"""
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "📥 Importar Datos al Sistema", 
            "", 
            "Archivos CSV (*.csv);;Todos los archivos (*)", 
            options=options
        )
        
        if file_name:
            success, message = self.sistema.importar_csv(file_name)
            if success:
                QMessageBox.information(self, "✅ Importación Exitosa", message)
                self.update_all_tables()
                self.dashboard.update_stats()
                self.update_system_info()
                self.statusBar().showMessage("✅ " + message, 5000)
            else:
                QMessageBox.warning(self, "❌ Error de Importación", message)
    
    def update_all_tables(self):
        """Actualiza todas las tablas del sistema"""
        self.students_tab.update_table()
        self.subjects_tab.update_table()
        self.profesores_tab.update_table()
        self.notes_tab.update_table()
        self.stats_tab.update_student_combo()
        self.stats_tab.update_subject_combo()
        self.stats_tab.update_ranking()
        self.stats_tab.update_risk_students()
        self.update_system_info()
    
    def closeEvent(self, event):
        """Evento al cerrar la ventana con confirmación"""
        reply = QMessageBox.question(self, "🚪 Confirmar Salida", 
                                   "¿Está seguro que desea cerrar el sistema?\n\nTodos los datos se guardarán automáticamente.",
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.sistema.guardar_datos()
            self.statusBar().showMessage("💾 Datos guardados correctamente", 1000)
            event.accept()
        else:
            event.ignore()