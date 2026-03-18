#!/bin/bash

# Enhanced Honeypot Dashboard Setup Script

echo "================================================"
echo "🛡  Honeypot Dashboard Setup"
echo "================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${BLUE}[1/5]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Check pip installation
echo -e "${BLUE}[2/5]${NC} Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed. Please install pip3.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}[3/5]${NC} Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Create templates directory
echo -e "${BLUE}[4/5]${NC} Setting up directory structure..."
mkdir -p templates
if [ -f "dashboard.html" ]; then
    mv dashboard.html templates/
    echo -e "${GREEN}✅ Moved dashboard.html to templates/${NC}"
fi

# Check for database
echo -e "${BLUE}[5/5]${NC} Checking database configuration..."
if [ -f "../database/attacks.db" ]; then
    echo -e "${GREEN}✅ Database found at ../database/attacks.db${NC}"
else
    echo -e "${YELLOW}⚠  Database not found at ../database/attacks.db${NC}"
    echo -e "${YELLOW}   Please update the DB path in app.py${NC}"
fi
echo ""

echo "================================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Update database path in app.py if needed:"
echo "   DB = '/path/to/your/attacks.db'"
echo ""
echo "2. Run the application:"
echo "   python3 app.py"
echo ""
echo "3. Open browser to:"
echo "   http://localhost:5000"
echo ""
echo "Optional - Test with simulated attacks:"
echo "   python3 simulate_attacks.py test"
echo ""
echo "For continuous simulation:"
echo "   python3 simulate_attacks.py continuous"
echo ""
echo "================================================"
