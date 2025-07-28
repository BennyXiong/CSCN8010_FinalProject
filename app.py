import subprocess
import os

def main():
    # Ensure correct path to the Streamlit script
    streamlit_script = os.path.join("src", "ui.py")
    
    # Launch Streamlit app
    subprocess.run(["streamlit", "run", streamlit_script])

if __name__ == "__main__":
    main()
