#!/usr/bin/env python3
"""
Script to convert all author fields in markdown files to the new standardized format:
author: ["Name (@github)", "Name (@github)"] for multiple authors
author: "Name (@github)" for single authors
"""

import os
import re
import glob

def convert_author_field(content):
    """Convert author field to new format."""
    
    # Pattern to match the old multi-line author objects
    multi_line_pattern = r'author:\s*\n\s*-\s*name:\s*"([^"]+)"(?:\s*\n\s*github:\s*"([^"]+)")?'
    
    # Pattern to match simple string author fields with @github format
    simple_pattern = r'author:\s*"([^"]+)"\s*\(@([^)]+)\)'
    
    # Pattern to match commented author fields with @github format
    commented_pattern = r'#\s*author:\s*"([^"]+)"\s*\(@([^)]+)\)'
    
    # Pattern to match empty author fields
    empty_pattern = r'author:\s*$'
    
    # Pattern to match simple author fields without github handle
    simple_no_github_pattern = r'author:\s*"([^"]+)"'
    
    # Pattern to match commented author fields without github handle
    commented_no_github_pattern = r'#\s*author:\s*"([^"]+)"'
    
    # Pattern to match commented empty author fields
    commented_empty_pattern = r'#\s*author:\s*""'
    
    # Replace multi-line author objects
    def replace_multi_line(match):
        name = match.group(1)
        github = match.group(2) if match.group(2) else ""
        if github:
            return f'author: "{name} (@{github})"'
        else:
            return f'author: "{name}"'
    
    # Replace simple string authors with github handle
    def replace_simple(match):
        name = match.group(1)
        github = match.group(2)
        return f'author: "{name} (@{github})"'
    
    # Replace commented authors with github handle
    def replace_commented(match):
        name = match.group(1)
        github = match.group(2)
        return f'# author: "{name} (@{github})"'
    
    # Replace simple authors without github handle
    def replace_simple_no_github(match):
        name = match.group(1)
        return f'author: "{name}"'
    
    # Replace commented authors without github handle
    def replace_commented_no_github(match):
        name = match.group(1)
        return f'# author: "{name}"'
    
    # Apply replacements
    content = re.sub(multi_line_pattern, replace_multi_line, content, flags=re.MULTILINE)
    content = re.sub(simple_pattern, replace_simple, content, flags=re.MULTILINE)
    content = re.sub(commented_pattern, replace_commented, content, flags=re.MULTILINE)
    content = re.sub(simple_no_github_pattern, replace_simple_no_github, content, flags=re.MULTILINE)
    content = re.sub(commented_no_github_pattern, replace_commented_no_github, content, flags=re.MULTILINE)
    content = re.sub(commented_empty_pattern, '# author: ""', content, flags=re.MULTILINE)
    
    # Replace empty author fields with a placeholder
    content = re.sub(empty_pattern, 'author: ""', content, flags=re.MULTILINE)
    
    return content

def process_file(file_path):
    """Process a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updated_content = convert_author_field(content)
        
        if original_content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⏭️  No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files."""
    # Get all markdown files in the docs directory, excluding 99-contribute and index.md
    docs_dir = os.path.join(os.getcwd(), "docs")
    md_files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)
    
    # Filter out 99-contribute directory and index.md files
    filtered_files = []
    for file_path in md_files:
        rel_path = os.path.relpath(file_path, docs_dir)
        if not rel_path.startswith("99-contribute") and not os.path.basename(file_path) == "index.md":
            filtered_files.append(file_path)
    
    print(f"Found {len(filtered_files)} markdown files to process...")
    
    updated_count = 0
    for file_path in filtered_files:
        if process_file(file_path):
            updated_count += 1
    
    print(f"\n🎉 Updated {updated_count} files out of {len(filtered_files)} total files.")

if __name__ == "__main__":
    main() 