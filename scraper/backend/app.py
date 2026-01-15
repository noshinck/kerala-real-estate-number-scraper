from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

class DataHarvester:
    def __init__(self):
        self.base_url = "https://rera.kerala.gov.in/agents"
        
    def setup_driver(self):
        """Setup headless Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def extract_data(self, limit=50):
        """Extract agent data from Kerala RERA"""
        driver = None
        results = []
        
        try:
            driver = self.setup_driver()
            driver.get(self.base_url)
            
            # Wait for page load
            time.sleep(5)
            
            # Try to find table
            tables = driver.find_elements(By.TAG_NAME, "table")
            
            if tables:
                rows = tables[0].find_elements(By.TAG_NAME, "tr")
                
                for i, row in enumerate(rows[1:limit+1]):  # Skip header
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if not cells:
                            continue
                        
                        text = ' | '.join([cell.text for cell in cells])
                        contact = self.parse_text(text)
                        
                        if contact and (contact['name'] or contact['email'] or contact['phone']):
                            results.append(contact)
                    except:
                        continue
            
            return results
            
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def parse_text(self, text):
        """Parse agent data from text"""
        contact = {
            'name': '',
            'phone': '',
            'email': '',
            'address': '',
            'category': ''
        }
        
        # Extract email
        email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email:
            contact['email'] = email.group()
        
        # Extract phone
        phone = re.search(r'[\d\s\-\(\)]{10,}', text)
        if phone:
            digits = re.sub(r'\D', '', phone.group())
            if len(digits) >= 10:
                contact['phone'] = '+91' + digits[-10:] if len(digits) == 10 else '+' + digits
        
        # Extract name - Kerala RERA pattern
        name_pattern = r'\d{10},,([A-Z][A-Za-z\s]+?)(?:\s*\||$)'
        name_match = re.search(name_pattern, text)
        if name_match:
            contact['name'] = name_match.group(1).strip()
        else:
            # Alternative pattern
            alt_pattern = r',,([^|,]+?)\s*\|'
            alt_match = re.search(alt_pattern, text)
            if alt_match:
                potential_name = alt_match.group(1).strip()
                if potential_name and not any(word in potential_name.lower() for word in ['individual', 'company', 'house', 'road']):
                    contact['name'] = potential_name
        
        # Extract category
        if 'Individual' in text:
            contact['category'] = 'Individual'
        elif 'Company' in text:
            contact['category'] = 'Company'
        elif 'Partnership' in text:
            contact['category'] = 'Partnership'
        elif 'Proprietor' in text:
            contact['category'] = 'Proprietorship'
        
        # Extract address
        address_pattern = r'\|\s*(?:Individual|Company|Partnership|Proprietor)\s*\|\s*(.+?)(?:$|\|)'
        addr_match = re.search(address_pattern, text)
        if addr_match:
            contact['address'] = addr_match.group(1).strip()
        
        return contact


# API Routes
@app.route('/api/extract', methods=['POST'])
def extract():
    """Main extraction endpoint"""
    try:
        data = request.get_json()
        source = data.get('source', 'kerala-rera')
        limit = data.get('limit', 50)
        
        # Validate inputs
        if source != 'kerala-rera':
            return jsonify({'error': 'Invalid data source'}), 400
        
        if not isinstance(limit, int) or limit < 1 or limit > 200:
            return jsonify({'error': 'Limit must be between 1 and 200'}), 400
        
        # Extract data
        harvester = DataHarvester()
        results = harvester.extract_data(limit)
        
        # Calculate statistics
        stats = {
            'total': len(results),
            'with_email': sum(1 for r in results if r['email']),
            'with_phone': sum(1 for r in results if r['phone']),
            'with_address': sum(1 for r in results if r['address'])
        }
        
        return jsonify({
            'success': True,
            'data': results,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'DataHarvest API'})


@app.route('/api/sources', methods=['GET'])
def sources():
    """Get available data sources"""
    return jsonify({
        'sources': [
            {
                'id': 'kerala-rera',
                'name': 'Kerala RERA Agents',
                'max_records': 823
            }
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)