from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from app.utils.supabase_client import fetch_health_history_questions

# Cache for the generated form class to avoid regenerating on every request
_cached_form_class = None  # Clear cache to force regeneration with new fields
_field_mapping = {}

def clear_form_cache():
    """Clear the cached form class to force regeneration."""
    global _cached_form_class, _field_mapping
    _cached_form_class = None
    _field_mapping = {}

def create_hhq_form_class():
    """Factory function to create a dynamic HHQ form class with fields from the database."""
    global _cached_form_class, _field_mapping
    
    if _cached_form_class is not None:
        return _cached_form_class
    
    # Base form fields that are always present
    form_attrs = {
        'next_step': SubmitField('Next'),
        'prev_step': SubmitField('Previous'),
        'save_exit': SubmitField('Save & Exit'),
        'submit_form': SubmitField('Submit'),
        'additional_notes': TextAreaField('Please provide any additional information or notes you would like to share:'),
    }
    
    # Add dynamic fields from database
    try:
        print("DEBUG: About to fetch health history questions...")
        questions = fetch_health_history_questions()
        print(f"DEBUG: fetch_health_history_questions returned: {type(questions)} with {len(questions) if questions else 'None'} items")
        
        if not questions:
            raise ValueError("No questions found in database")
            
        print(f"Generated {len(questions)} dynamic fields for HHQ form")
        for question in questions:
            if not question.get('variable_name'):
                print(f"Warning: Question missing variable_name: {question}")
                continue
                
            db_variable_name = question['variable_name']
            form_field_name = db_variable_name.replace('-', '_')
            question_text = question.get('question_text', question.get('display_text', db_variable_name))
            
            if not question_text:
                print(f"Warning: Question missing text: {db_variable_name}")
                continue
            
            # Store the mapping
            _field_mapping[form_field_name] = db_variable_name
            
            # Determine field type based on variable name or question content
            if db_variable_name in ['hh-height', 'hh-weight']:
                # Use StringField for height and weight
                form_attrs[form_field_name] = StringField(
                    question_text,
                    description=question.get('description', ''),
                    validators=[DataRequired()] if question.get('required', False) else []
                )
                print(f"DEBUG: Created StringField for {db_variable_name}")
            else:
                # Use BooleanField for all other questions (existing behavior)
                form_attrs[form_field_name] = BooleanField(
                    question_text,
                    description=question.get('description', ''),
                    validators=[DataRequired()] if question.get('required', False) else []
                )
            
        print(f"DEBUG: Successfully added {len(_field_mapping)} dynamic fields to form class")
    except Exception as e:
        print(f"Error generating dynamic fields: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    # Add helper methods to the form class
    def get_db_field_name(self, form_field_name):
        """Convert form field name back to database variable name."""
        return _field_mapping.get(form_field_name, form_field_name)
    
    def get_form_field_name(self, db_variable_name):
        """Convert database variable name to form field name."""
        # First check if we have a mapping
        for form_name, db_name in _field_mapping.items():
            if db_name == db_variable_name:
                return form_name
        # Fall back to simple replacement if no mapping found
        return db_variable_name.replace('-', '_')
    
    def validate_section(self, section_name):
        """Validate all fields in a given section."""
        section_fields = get_section_fields(section_name)
        for field_name in section_fields:
            form_field_name = self.get_form_field_name(field_name)
            if hasattr(self, form_field_name):
                field = getattr(self, form_field_name)
                if field.validators and not field.validate(self):
                    return False
        return True
    
    form_attrs['get_db_field_name'] = get_db_field_name
    form_attrs['get_form_field_name'] = get_form_field_name
    form_attrs['validate_section'] = validate_section
    
    # Create the dynamic form class
    _cached_form_class = type('HHQForm', (FlaskForm,), form_attrs)
    return _cached_form_class

def HHQForm(*args, **kwargs):
    """Factory function that returns an instance of the dynamically created form class."""
    form_class = create_hhq_form_class()
    return form_class(*args, **kwargs) 