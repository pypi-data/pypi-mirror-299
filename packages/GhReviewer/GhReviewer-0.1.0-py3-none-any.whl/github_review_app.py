import sys
import os
import requests
import pandas as pd
import re
import pickle
import logging
from PyQt5.QtCore import (
    QUrl, Qt, QTimer, QPropertyAnimation, pyqtProperty, QThread, pyqtSignal, QObject, QThreadPool, QRunnable, QEventLoop
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog, QInputDialog,
    QMainWindow, QGraphicsOpacityEffect
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

logging.basicConfig(level=logging.INFO)
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QInputDialog, 
                             QMessageBox, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class ToastLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background-color: #323232;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setWindowFlags(Qt.ToolTip)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self._opacity = 0.0
        self.opacity_effect.setOpacity(self._opacity)
        self.animation = QPropertyAnimation(self, b"opacity", self)
        self.hide()

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.opacity_effect.setOpacity(self._opacity)

    def getOpacity(self):
        return self._opacity

    opacity = pyqtProperty(float, getOpacity, setOpacity)

    def show_message(self, message, duration=2000):
        self.setText(message)
        self.adjustSize()
        self.move(
            int(self.parent().width() / 2 - self.width() / 2),
            int(self.parent().height() - self.height() - 50)
        )
        self.show()
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
        QTimer.singleShot(duration, self.hide_toast)

    def hide_toast(self):
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.hide)
        self.animation.start()


class CustomWebEngineView(QWebEngineView):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.is_loading_markdown = False
        self.urlChanged.connect(self.on_url_changed)

    def on_url_changed(self, url):
        if self.is_loading_markdown:
            return

        if url.toString().endswith('.md'):
            self.is_loading_markdown = True
            self.app.load_and_render_markdown(url)
        else:
            QDesktopServices.openUrl(url)
            self.is_loading_markdown = False
            self.back()

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            if url.toString().endswith('.md'):
                self.app.load_and_render_markdown(url)
            else:
                QDesktopServices.openUrl(url)
            return False
        return True 


light_mode_css = """
        <style>
        a {
            color: #1e90ff;
        }
        code, pre {
            background-color: #3c3f41;
            color: #ffffff;
        }
        table {
            background-color: #3c3f41;
            color: #ffffff;
        }
        blockquote {
            background-color: #3c3f41;
            border-left: 5px solid #5c5c5c;
            padding: 10px;
            color: #ffffff;
        }
        img {
            filter: brightness(0.8);
        }
        </style>
        """

dark_mode_css = """
        <style>
        body {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        a {
            color: #1e90ff;
        }
        code, pre {
            background-color: #3c3f41;
            color: #ffffff;
        }
        table {
            background-color: #3c3f41;
            color: #ffffff;
        }
        blockquote {
            background-color: #3c3f41;
            border-left: 5px solid #5c5c5c;
            padding: 10px;
            color: #ffffff;
        }
        img {
            filter: brightness(0.8);
        }
        </style>
        """

light_style = """

QWidget {
    background-color: #f0f0f0;
    color: #000000;
    font-size: 14px;
}
QLabel {
    font-size: 14px;
    color: #000000;
}
QPushButton {
    background-color: #ffffff;
    border: 1px solid #bfbfbf;
    padding: 6px 12px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #e6e6e6;
}
QLineEdit, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #bfbfbf;
    padding: 4px;
    font-size: 14px;
}
QScrollBar:vertical {
    background-color: #f0f0f0;
}
QScrollBar::handle:vertical {
    background-color: #c0c0c0;
}
QPushButton#includeButton {
    background-color: #28a745;
    color: #ffffff;
    border: none;
    padding: 6px 12px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#includeButton:hover {
    background-color: #218838;
}
QPushButton#excludeButton {
    background-color: #dc3545;
    color: #ffffff;
    border: none;
    padding: 6px 12px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#excludeButton:hover {
    background-color: #c82333;
}
"""

dark_style = """

QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-size: 14px;
}
QLabel {
    font-size: 14px;
    color: #ffffff;
}
QPushButton {
    background-color: #3c3f41;
    border: 1px solid #5c5c5c;
    padding: 6px 12px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #4b4b4b;
}
QLineEdit, QTextEdit {
    background-color: #3c3f41;
    border: 1px solid #5c5c5c;
    padding: 4px;
    font-size: 14px;
}
QScrollBar:vertical {
    background-color: #2b2b2b;
}
QScrollBar::handle:vertical {
    background-color: #5c5c5c;
}
QPushButton#includeButton {
    background-color: #28a745;
    color: #ffffff;
    border: none;
    padding: 6px 12px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#includeButton:hover {
    background-color: #218838;
}
QPushButton#excludeButton {
    background-color: #dc3545;
    color: #ffffff;
    border: none;
    padding: 6px 12px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#excludeButton:hover {
    background-color: #c82333;
}
"""

class Worker(QObject):
    data_loaded = pyqtSignal(pd.DataFrame)
    readme_loaded = pyqtSignal(str, str)  # full_name, readme_html

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)

class ReadmePrefetcher(QRunnable):
    def __init__(self, app, full_name):
        super().__init__()
        self.app = app
        self.full_name = full_name

    def run(self):
        self.app.get_readme_html(self.full_name)

class GitHubReviewApp(QMainWindow):
    def __init__(self, token=None, csv_file=None, masked=False):
        super().__init__()
        self.token = token
        self.csv_file = csv_file
        self.masked = masked  # For the --masked flag
        self.data = pd.DataFrame()
        self.current_index = 0
        self.readme_cache = {}
        self.included_count = 0

        self.threads = []
        self.threadpool = QThreadPool()

        self.init_ui()

    def open_link_in_browser(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def update_readme_view(self):
        full_name = self.current_repo_full_name
        if full_name in self.readme_cache:
            readme_html = self.readme_cache[full_name]
            if self.dark_mode:
                readme_html = self.inject_dark_mode_css(readme_html)
            self.readme_view.setHtml(readme_html)


    def toggle_dark_mode(self, checked):
        if checked:
            self.dark_mode = True
            self.apply_stylesheet(dark_style)
        else:
            self.dark_mode = False
            self.apply_stylesheet(light_style)
        self.update_readme_view()


    def apply_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)

    def init_ui(self):
        self.setWindowTitle('GitHub Repository Review')
        self.apply_stylesheet(light_style)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.name_label = QLabel('Repository Name')
        self.name_label.setObjectName('nameLabel')
        self.name_label.setStyleSheet('font-size: 18pt; font-weight: bold; text-decoration:none;')
        self.name_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.name_label.setOpenExternalLinks(True)

        self.counter_label = QLabel('Included: 0')
        self.counter_label.setAlignment(Qt.AlignLeft)
        self.counter_label.setStyleSheet('font-size: 14px;')

        self.progress_label = QLabel('Repository 1 of N')
        self.progress_label.setAlignment(Qt.AlignRight)
        self.progress_label.setStyleSheet('font-size: 14px;')

        self.dark_mode = False
        self.toggle_button = QPushButton('Toggle Dark Mode')
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggled.connect(self.toggle_dark_mode)
        self.toggle_button.setStyleSheet('font-size: 14px;')

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.name_label)
        
        header_layout.addStretch()
        header_layout.addWidget(self.progress_label)
        header_layout.addSpacerItem(QSpacerItem(5, 20, QSizePolicy.Expanding, QSizePolicy.Fixed))

        header_layout.addWidget(self.counter_label)
        header_layout.addSpacerItem(QSpacerItem(5, 20, QSizePolicy.Expanding, QSizePolicy.Fixed))
        header_layout.addWidget(self.toggle_button)

        self.description_label = QLabel('Repository Description')
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet('font-size: 14px;')

        self.readme_view = QWebEngineView()
        self.readme_page = CustomWebEnginePage(self, self.readme_view)
        self.readme_view.setPage(self.readme_page)

        self.comment_label = QLabel('Motivation / Comments:')
        self.comment_edit = QTextEdit()

        self.include_button = QPushButton('Include (i)')
        self.include_button.setObjectName('includeButton')
        self.include_button.clicked.connect(self.include_repository)

        self.exclude_button = QPushButton('Exclude (e)')
        self.exclude_button.setObjectName('excludeButton')
        self.exclude_button.clicked.connect(self.exclude_repository)

        self.prev_button = QPushButton('Previous')
        self.prev_button.clicked.connect(self.prev_repository)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_repository)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.readme_view, stretch=4)
        main_layout.addWidget(self.comment_label)
        main_layout.addWidget(self.comment_edit, stretch=1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.include_button)
        button_layout.addWidget(self.exclude_button)
        main_layout.addLayout(button_layout)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        main_layout.addLayout(nav_layout)

        self.toast = ToastLabel(self)

        self.load_readme_cache()

        if not self.token:
            self.token, ok = QInputDialog.getText(self, 'GitHub Token', 'Enter your GitHub Personal Access Token:')
            if not ok or not self.token:
                QMessageBox.warning(self, 'Token Required', 'A GitHub token is required to proceed.')
                sys.exit(1)

        if self.csv_file and os.path.isfile(self.csv_file):
            self.load_data_from_csv(self.csv_file)
            self.load_repository()
        else:
            queries, ok = QInputDialog.getMultiLineText(self, 'Search Queries', 'Enter your search queries (one per line):')
            if not ok or not queries.strip():
                QMessageBox.warning(self, 'Search Queries Required', 'At least one search query is required to proceed.')
                sys.exit(1)
            self.search_queries = [q.strip() for q in queries.strip().split('\n') if q.strip()]
            self.run_searches_thread()

        if 'Include' not in self.data.columns:
            self.data['Include'] = ''
        if 'Comment' not in self.data.columns:
            self.data['Comment'] = ''

        if self.masked:
            self.name_label.hide() 

        self.showMaximized()

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_E:
                self.include_repository()
            elif event.key() == Qt.Key_Q:
                self.exclude_repository()
        elif event.key() == Qt.Key_Left:
            self.prev_repository()
        elif event.key() == Qt.Key_Right:
            self.next_repository()
        else:
            super().keyPressEvent(event)

    def run_searches_thread(self):
        self.search_thread = QThread()
        self.worker = Worker(self.run_searches)
        self.worker.moveToThread(self.search_thread)
        self.search_thread.started.connect(self.worker.run)
        self.worker.data_loaded.connect(self.on_data_loaded)
        self.search_thread.start()
        self.threads.append(self.search_thread)

    def run_searches(self):
        all_repos = []
        for query in self.search_queries:
            repos = self.search_github(query, self.token)
            all_repos.extend(repos)
        if all_repos:
            data = pd.DataFrame(all_repos)
            data.drop_duplicates(subset='full_name', inplace=True)
            data.sort_values(by='stargazers_count', ascending=False, inplace=True)
            data.reset_index(drop=True, inplace=True)
            data['Include'] = ''
            self.worker.data_loaded.emit(data)
        else:
            self.worker.data_loaded.emit(pd.DataFrame())

    def on_data_loaded(self, data):
        self.data = data
        if self.data.empty:
            QMessageBox.information(self, 'No Results', 'No repositories found from the search queries.')
            sys.exit(0)
        else:
            self.included_count = self.data[self.data['Include'] == 'Yes'].shape[0]
            self.update_counter_label()
            self.load_repository()
        self.search_thread.quit()
        self.search_thread.wait()

    def search_github(self, query, token):
        headers = {'Authorization': f'token {token}'}
        url = 'https://api.github.com/search/repositories'
        params = {
            'q': query,
            'per_page': 100,
            'page': 1
        }
        results = []

        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                QMessageBox.warning(self, 'Error', f'GitHub API Error: {response.status_code} {response.text}')
                break
            data = response.json()
            items = data.get('items', [])
            results.extend(items)

            if 'next' in response.links:
                params['page'] += 1
            else:
                break

            if len(results) >= 1000:
                QMessageBox.information(self, 'Limit Reached', 'Reached maximum number of results (1000).')
                break

        return results

    def update_counter_label(self):
        self.counter_label.setText(f'Included: {self.included_count}')

    def load_repository(self):
        if self.current_index >= len(self.data):
            QMessageBox.information(self, 'End', 'No more repositories to display.')
            return
        self.comment_edit.clear()
        repo = self.data.iloc[self.current_index]
        self.current_repo_full_name = repo['full_name']

        if not self.masked:
            self.name_label.setText(f"<a href='{repo['html_url']}'>{repo['full_name']}</a>")
            self.name_label.setOpenExternalLinks(True)
        else:
            self.name_label.setText('Repository Name Hidden')
        self.description_label.setText(repo.get('description', 'No description provided.'))

        total = len(self.data)
        self.progress_label.setText(f'Repository {self.current_index + 1} of {total}')

        self.load_readme_thread(repo['full_name'])

        if isinstance(repo.get('Comment'), str):
            self.comment_edit.setText(repo.get('Comment'))

    def load_readme_thread(self, full_name):
        self.readme_thread = QThread()
        self.readme_worker = Worker(self.load_readme_async, full_name)
        self.readme_worker.moveToThread(self.readme_thread)
        self.readme_worker.readme_loaded.connect(self.on_readme_loaded)
        self.readme_thread.started.connect(self.readme_worker.run)
        self.readme_thread.start()
        self.threads.append(self.readme_thread)

    def load_readme_async(self, full_name):
        readme_html = self.get_readme_html(full_name)
        self.readme_worker.readme_loaded.emit(full_name, readme_html)

    def on_readme_loaded(self, full_name, readme_html):
        if self.current_repo_full_name == full_name:
            if self.dark_mode:
                readme_html = self.inject_dark_mode_css(readme_html)
            else:
                readme_html = self.inject_light_mode_css(readme_html)
            self.readme_view.setHtml(readme_html)
        self.readme_thread.quit()
        self.readme_thread.wait()
        self.prefetch_next_readme()


    def prefetch_next_readme(self):
        if self.current_index + 1 < len(self.data):
            next_repo = self.data.iloc[self.current_index + 1]
            full_name = next_repo['full_name']
            if full_name not in self.readme_cache:
                prefetch_task = ReadmePrefetcher(self, full_name)
                self.threadpool.start(prefetch_task)

    def inject_light_mode_css(self, html_content):
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', light_mode_css + '</head>')
        else:
            html_content = light_mode_css + html_content
        return html_content

    def inject_dark_mode_css(self, html_content):
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', dark_mode_css + '</head>')
        else:
            html_content = dark_mode_css + html_content
        return html_content


    def load_and_render_markdown(self, url):
        raw_url = url.toString().replace('blob', 'raw')

        response = requests.get(raw_url)
        if response.status_code == 200:
            markdown_content = response.text

            html_content = self.get_rendered_markdown_from_github(markdown_content)

            html_content = self.clean_readme_content(html_content, self.current_repo_full_name)

            if self.dark_mode:
                html_content = self.inject_dark_mode_css(html_content)
            self.readme_view.setHtml(html_content)

        else:
            QMessageBox.warning(self, 'Error', f'Failed to load {url.url()}')

    def get_readme_html(self, full_name):
        if full_name in self.readme_cache:
            logging.info(f'Using cached README for {full_name}')
            return self.readme_cache[full_name]

        default_branch = self.get_default_branch(full_name)

        api_url = f'https://api.github.com/repos/{full_name}/readme'
        headers = {'Authorization': f'token {self.token}', 'Accept': 'application/vnd.github.v3.raw'}
        params = {'ref': default_branch}
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            markdown_text = response.text

            html = self.get_rendered_markdown_from_github(markdown_text)
            html = self.rewrite_relative_links(html, full_name, default_branch)

            html = self.clean_readme_content(html, full_name)

            self.readme_cache[full_name] = html
            return html
        else:
            html = '<h1>No README.md found.</h1>'
            self.readme_cache[full_name] = html
            return html

    def rewrite_relative_links(self, html_content, repo_full_name, branch='main'):
        base_url = f'https://raw.githubusercontent.com/{repo_full_name}/{branch}/'
        repo_url = f'https://github.com/{repo_full_name}/blob/{branch}/'

        html_content = re.sub(
            r'(<a\s+[^>]*href\s*=\s*["\'])(?!http|https|mailto|#)([^"\']+)(["\'])',
            lambda match: (
                f'{match.group(1)}{repo_url}{match.group(2)}{match.group(3)}'
                if match.group(2).endswith('.md')
                else f'{match.group(1)}{base_url}{match.group(2)}{match.group(3)}'
            ),
            html_content
        )

        html_content = re.sub(
            r'(<img\s+[^>]*src\s*=\s*["\'])(?!http|https)([^"\']+)(["\'])',
            lambda match: f'{match.group(1)}{base_url}{match.group(2)}{match.group(3)}',
            html_content
        )

        return html_content

    def get_rendered_markdown_from_github(self, markdown_text):
        url = 'https://api.github.com/markdown'
        headers = {'Authorization': f'token {self.token}', 'Content-Type': 'application/json'}
        payload = {
            'text': markdown_text,
            'mode': 'gfm'
        }
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.text
        else:
            return '<h1>Error rendering Markdown</h1>'

    def get_default_branch(self, full_name):
        api_url = f'https://api.github.com/repos/{full_name}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('default_branch', 'master')
        else:
            return 'master'

    def include_repository(self):
        if self.data.at[self.current_index, 'Include'] != 'Yes':
            self.included_count += 1
        self.data.at[self.current_index, 'Include'] = 'Yes'
        self.data.at[self.current_index, 'Comment'] = self.comment_edit.toPlainText()
        self.update_counter_label()
        self.save_progress()
        self.toast.show_message("Repository included")
        self.next_repository()

    def exclude_repository(self):
        if self.data.at[self.current_index, 'Include'] == 'Yes':
            self.included_count -= 1
        self.data.at[self.current_index, 'Include'] = 'No'
        self.data.at[self.current_index, 'Comment'] = self.comment_edit.toPlainText()
        self.update_counter_label()
        self.save_progress()
        self.toast.show_message("Repository excluded")
        self.next_repository()

    def next_repository(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.load_repository()
        else:
            QMessageBox.information(self, 'End', 'This is the last repository.')
            self.save_progress()
            self.save_readme_cache()

    def prev_repository(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_repository()
        else:
            QMessageBox.information(self, 'Start', 'This is the first repository.')


    def clean_readme_content(self, html_content, repo_full_name):
        if not self.masked:
            return html_content

        repo_name = repo_full_name.split('/')[-1]
        repo_owner = repo_full_name.split('/')[0]

        patterns = [
            re.escape(repo_full_name),
            re.escape(repo_name),
            re.escape(repo_owner)
        ]

        pattern = '|'.join(patterns)
        regex = re.compile(pattern, re.IGNORECASE)
        html_content = regex.sub('[REDACTED]', html_content)

        html_content = re.sub(r'<img[^>]*>', '', html_content)

        return f"<div class=\"highlight highlight-source-shell\"> {html_content} </div>"


    def save_progress(self):
        if not self.csv_file:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
            if filename:
                if not filename.endswith('.csv'):
                    filename += '.csv'
                self.csv_file = filename
            else:
                QMessageBox.warning(self, 'Save Cancelled', 'Save operation was cancelled.')
                return
        self.data.to_csv(self.csv_file, index=False)

    def load_data_from_csv(self, csv_file):
        self.data = pd.read_csv(csv_file)
        if 'Include' not in self.data.columns:
            self.data['Include'] = ''
        if 'Comment' not in self.data.columns:
            self.data['Comment'] = ''
        self.data.reset_index(drop=True, inplace=True)
        self.included_count = self.data[self.data['Include'] == 'Yes'].shape[0]
        self.update_counter_label()

    def save_readme_cache(self):
        cache_file = 'readme_cache.pkl'
        with open(cache_file, 'wb') as f:
            pickle.dump(self.readme_cache, f)

    def load_readme_cache(self):
        cache_file = 'readme_cache.pkl'
        if os.path.isfile(cache_file):
            with open(cache_file, 'rb') as f:
                self.readme_cache = pickle.load(f)
        else:
            self.readme_cache = {}

    def closeEvent(self, event):
        for thread in self.threads:
            thread.quit()
            thread.wait()
        self.threadpool.waitForDone()
        super().closeEvent(event)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='GitHub Repository Review Application')
    parser.add_argument('--token', help='GitHub Personal Access Token')
    parser.add_argument('--csv', help='CSV file to load')
    parser.add_argument('--masked', action='store_true', help='Enable masked mode to hide repository names and images')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    review_app = GitHubReviewApp(token=args.token, csv_file=args.csv, masked=args.masked)
    review_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
