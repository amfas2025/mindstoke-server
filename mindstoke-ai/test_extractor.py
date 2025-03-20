from app.utils.lab_extractor import process_pdf, save_results
import os

def test_lab_extraction():
    # Test with a single PDF file
    pdf_path = "client_labs/sample.pdf"  # Replace with your actual PDF file
    
    if os.path.exists(pdf_path):
        print(f"Processing {pdf_path}...")
        results = process_pdf(pdf_path)
        
        if results:
            print("\nExtracted Lab Results:")
            for test, value in results.items():
                print(f"{test}: {value}")
            
            # Save results to CSV
            client_id = os.path.splitext(os.path.basename(pdf_path))[0]
            save_results(client_id, results, "extracted_results")
            print("\nResults have been saved to CSV in the extracted_results directory")
        else:
            print("No results were extracted from the PDF")
    else:
        print(f"Please place a PDF file at {pdf_path}")

if __name__ == "__main__":
    test_lab_extraction() 