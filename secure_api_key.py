"""
Script to secure API key before pushing to GitHub
Run this before your first git push!
"""

import os
import re

def secure_file(filepath, old_pattern, new_content):
    """Replace API key with environment variable"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the pattern
        new_content_full = re.sub(old_pattern, new_content, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content_full)
        
        print(f"✅ Secured: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error securing {filepath}: {e}")
        return False

def create_env_file(api_key):
    """Create .env file with API key"""
    try:
        with open('.env', 'w') as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        print("✅ Created .env file")
        return True
    except Exception as e:
        print(f"❌ Error creating .env: {e}")
        return False

def main():
    print("=" * 60)
    print("🔐 SECURING API KEY FOR GITHUB")
    print("=" * 60)
    print()
    
    # The API key to secure
    api_key = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"
    
    # 1. Secure ai_detection.py
    print("Step 1: Securing ai_detection.py...")
    pattern1 = r'GEMINI_API_KEY = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"'
    replacement1 = 'GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")'
    secure_file('ai_detection.py', pattern1, replacement1)
    
    # 2. Secure aiDetection.ts
    print("\nStep 2: Securing aiDetection.ts...")
    pattern2 = r'const GEMINI_API_KEY = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"'
    replacement2 = 'const GEMINI_API_KEY = process.env.NEXT_PUBLIC_GEMINI_API_KEY || ""'
    secure_file('aiDetection.ts', pattern2, replacement2)
    
    # 3. Create .env file
    print("\nStep 3: Creating .env file...")
    create_env_file(api_key)
    
    # 4. Verify .gitignore exists
    print("\nStep 4: Checking .gitignore...")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print("✅ .env is in .gitignore")
            else:
                print("⚠️  Adding .env to .gitignore...")
                with open('.gitignore', 'a') as f:
                    f.write('\n.env\n')
                print("✅ Added .env to .gitignore")
    else:
        print("❌ .gitignore not found!")
    
    print()
    print("=" * 60)
    print("✅ API KEY SECURED!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the changes in ai_detection.py and aiDetection.ts")
    print("2. Make sure .env file exists (it should NOT be committed)")
    print("3. Run: git add .")
    print("4. Run: git commit -m 'Secure API key'")
    print("5. Run: git push")
    print()
    print("⚠️  IMPORTANT: Never commit the .env file to GitHub!")
    print()

if __name__ == "__main__":
    main()
