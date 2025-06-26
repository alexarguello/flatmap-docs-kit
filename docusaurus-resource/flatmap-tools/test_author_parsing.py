#!/usr/bin/env python3
"""
Test script to verify author parsing works correctly with the new format.
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from util import parse_frontmatter
from generate_collaborate_pages import get_author_info

def test_author_parsing():
    """Test author parsing with various formats."""
    
    test_cases = [
        # Format: "Name (@github)"
        'author: "Lize Raes (@lizeraes)"',
        'author: "Jane Doe (@janedoe)"',
        'author: "Dr. Alice Nguyen (@aliceng)"',
        
        # Format: ["Name (@github)", "Name (@github)"] (multiple authors)
        'author: ["Lize Lala (@lizela)", "Data Science Central (@datasciencecentral)"]',
        
        # Format: "Name" (no github handle)
        'author: "John Smith"',
        
        # Empty author
        'author: ""',
        
        # Commented author
        '# author: "Lize Raes (@lizeraes)"',
    ]
    
    print("Testing author parsing...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case}")
        
        # Create a temporary frontmatter content
        frontmatter_content = f"""---
title: Test Article
status: draft
{test_case}
---
"""
        
        # Write to temporary file
        temp_file = f"temp_test_{i}.md"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter_content)
        
        try:
            # Parse frontmatter
            parsed = parse_frontmatter(temp_file)
            author_field = parsed.get('author', '')
            print(f"  Parsed author field: {repr(author_field)}")
            
            # Test get_author_info
            if author_field:
                author_name, author_handle = get_author_info(author_field)
                print(f"  Author name: {repr(author_name)}")
                print(f"  Author handle: {repr(author_handle)}")
            else:
                print(f"  No author field found")
                
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    test_author_parsing() 