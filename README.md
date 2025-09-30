# JobTracker Pro - Modern Job Application Tracker

A comprehensive Django-based job application tracking system with a modern dark theme interface.

## ✨ Features

### 🎨 Modern Dark Theme UI
- **Professional Dark Design**: Sleek dark theme optimized for readability and reduced eye strain
- **Modern Typography**: Inter font family for excellent readability across all devices
- **Smooth Animations**: CSS transitions and hover effects for enhanced user experience
- **Responsive Design**: Fully responsive layout that works perfectly on desktop, tablet, and mobile
- **Accessible**: WCAG compliant with proper contrast ratios and focus states

### 🚀 Core Functionality
- **Application Management**: Track job applications with detailed status updates
- **Company Profiles**: Maintain comprehensive company information
- **Document Management**: Upload and organize resumes, cover letters, and other documents
- **Interview Scheduling**: Keep track of upcoming interviews and rounds
- **Analytics Dashboard**: Visual insights into your job search progress
- **Email Integration**: Send application emails directly from the platform

### 🔧 Technical Features
- **Django 5.2**: Latest Django framework for robust backend
- **Bootstrap 5.3**: Modern responsive CSS framework
- **Interactive Components**: Enhanced forms, dropdowns, and navigation
- **Static File Management**: Optimized CSS and JavaScript delivery
- **Database Integration**: SQLite for development, easily configurable for production

## 🎨 UI Improvements Made

### Design System
- **Color Palette**: Carefully crafted dark theme with excellent contrast
- **Component Library**: Consistent styling across all UI elements
- **Typography Scale**: Hierarchical text sizing and weights
- **Spacing System**: Harmonious spacing using CSS custom properties

### User Experience
- **Navigation**: Intuitive navigation with active states and breadcrumbs
- **Dashboard**: Clean overview with statistics cards and recent activity
- **Forms**: Enhanced form styling with better validation feedback
- **Loading States**: Smooth loading animations and skeleton screens
- **Hover Effects**: Subtle animations that provide visual feedback

### Accessibility
- **Keyboard Navigation**: Full keyboard accessibility support
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Focus Management**: Clear focus indicators for all interactive elements
- **High Contrast**: Excellent color contrast ratios throughout

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd interview_tracker
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
interview_tracker/
├── interview_tracker/          # Django project settings
├── jobs/                       # Main application
│   ├── templates/jobs/         # HTML templates with modern dark theme
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   └── urls.py                # URL routing
├── static/                     # Static files
│   ├── css/
│   │   └── dark-theme.css     # Modern dark theme styles
│   └── js/
│       └── app.js             # Enhanced JavaScript interactions
└── manage.py                  # Django management script
```

## 🎯 Key Pages

- **Dashboard**: Overview with statistics and recent applications
- **Applications List**: Manage all job applications with search and filters
- **Application Forms**: Create and edit applications with modern form styling
- **Company Management**: Add and manage company profiles
- **Document Upload**: Handle resumes and cover letters
- **Analytics**: Visual insights into application progress

## 🔧 Customization

The UI can be easily customized by modifying the CSS custom properties in `/static/css/dark-theme.css`:

```css
:root {
    /* Colors can be customized here */
    --accent-primary: #58a6ff;
    --accent-success: #56d364;
    /* ... */
}
```

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.