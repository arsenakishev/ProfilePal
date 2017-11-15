#Imran Ahmed
#ProfilePal
import ResumeParser

def main():
    f = ResumeParser.parseResume("jDoeResume.docx","C:\Users\Imran\Desktop\jDoeResume.docx")
    print("DOCX:\n")
    print(f)
    a = ResumeParser.parseResume("jDoeResume.pdf","C:\Users\Imran\Desktop\jDoeResume.pdf")
    print("PDF:\n")
    print(a)
    b_json = ResumeParser.parseResume("jDoeResume.txt","C:\Users\Imran\Desktop\jDoeResume.txt")
    print("TXT:\n")
    print(b_json)
main()
