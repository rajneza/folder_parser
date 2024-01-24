# %%writefile /content/resume_parser/resume_parser/resumeparse.py
# !apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-resumeparse pstotext tesseract-ocr
# !sudo apt-get install libenchant1c2a


# !pip install tika
# !pip install docx2txt
# !pip install phonenumbers
# !pip install pyenchant
# !pip install stemming

#from _future_ import division
import nltk
import aspose.words as aw

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')

import re
import os
import shutil
from datetime import date

import nltk
import docx2txt
import pandas as pd

import phonenumbers
import pdfplumber

import logging

import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher


import sys
import operator
import string
import nltk
from stemming.porter2 import stem
import mysql.connector

# load pre-trained model
base_path = os.path.dirname(__file__)


nlp = spacy.load('en_core_web_sm')

custom_nlp2 = spacy.load(os.path.join(base_path,"degree","model"))
custom_nlp3 = spacy.load(os.path.join(base_path,"company_working","model"))

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

# The below 6 line code is to extract designation
file = os.path.join(base_path,"titles_combined.txt")
file = open(file, "r", encoding='utf-8')
designation = [line.strip().lower() for line in file]
designitionmatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in designation if len(nlp.make_doc(text)) < 10]
designitionmatcher.add("Job title", None, *patterns)
                        
# The below 6 line code is to extract skills
file = os.path.join(base_path,"LINKEDIN_SKILLS_ORIGINAL.txt") 
file = open(file, "r", encoding='utf-8')    
skill = [line.strip().lower() for line in file]
skillsmatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in skill if len(nlp.make_doc(text)) < 10]
skillsmatcher.add("Job title", None, *patterns)


class resumeparse(object):
    def extract_projects(text):
        """
        Extract project details from the given text.
        You may need to adapt this function based on how project details are presented in your resume.

        Parameters:
        - text (str): The text containing information about projects.

        Returns:
        - List of project details.
        """
        projects = []
        project_starts = re.finditer(r'Project[^\w\n](\w[^\n])', text, re.IGNORECASE)
        
        for start_match in project_starts:
            project_start = start_match.group(1)
            project_end_match = re.search(r'(?:(?:Project|Objective|Work and Employment|Education and Training|Skills|Accomplishments|Misc):|$)', project_start, re.IGNORECASE)
            
            if project_end_match:
                project_end_index = project_end_match.start()
                project_details = project_start[:project_end_index].strip()
                projects.append(project_details)

        return projects
       
    objective = (
        'career goal',
        'objective',
        'career objective',
        'employment objective',
        'professional objective',        
        'career summary',
        'professional summary',
        'summary of qualifications',
        'summary',
        # 'digital'
    )

    work_and_employment = (
        'career profile',
        'employment history',
        'work history',
        'work experience',
        'experience',
        'professional experience',
        'professional background',
        'additional experience',
        'career related experience',
        'related experience',
        'programming experience',
        'freelance',
        'freelance experience',
        'army experience',
        'military experience',
        'military background',
    )

    education_and_training = (
        'academic background',
        'academic experience',
        'programs',
        'courses',
        'related courses',
        'education',
        'qualifications',
        'educational background',
        'educational qualifications',
        'educational training',
        'education and training',
        'training',
        'academic training',
        'professional training',
        'course project experience',
        'related course projects',
        'internship experience',
        'internships',
        'apprenticeships',
        'college activities',
        'certifications',
        'special training',
    )

    skills_header = (
        'credentials',
        'areas of experience',
        'areas of expertise',
        'areas of knowledge',
        'skills',
        "other skills",
        "other abilities",
        'career related skills',
        'professional skills',
        'specialized skills',
        'technical skills',
        'computer skills',
        'personal skills',
        'computer knowledge',        
        'technologies',
        'technical experience',
        'proficiencies',
        'languages',
        'language competencies and skills',
        'programming languages',
        'competencies'
    )

    misc = (
        'activities and honors',
        'activities',
        'affiliations',
        'professional affiliations',
        'associations',
        'professional associations',
        'memberships',
        'professional memberships',
        'athletic involvement',
        'community involvement',
        'refere',
        'civic activities',
        'extra-Curricular activities',
        'professional activities',
        'volunteer work',
        'volunteer experience',
        'additional information',
        'interests'
    )

    accomplishments = (
        'achievement',
        'licenses',
        'presentations',
        'conference presentations',
        'conventions',
        'dissertations',
        'exhibits',
        'papers',
        'publications',
        'professional publications',
        'research',
        'research grants',
        'project',
        'research projects',
        'personal projects',
        'current research interests',
        'thesis',
        'theses',
    )
       

           
    def convert_docx_to_txt(docx_file):
        """
            A utility function to convert a Microsoft docx files to raw text.

            This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
            :param docx_file: docx file with gets uploaded by the user
            :type docx_file: InMemoryUploadedFile
            :return: The text contents of the docx file
            :rtype: str
        """
        try:
            print(docx_file)
            text = docx2txt.process(docx_file)  # Extract text from docx file
            print("242")
            # txt_file = "./True_Talent.txt"

            # with open(txt_path, 'w', encoding='utf-8') as txt_file:
            #     txt_file.write(text)
            
            clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            print("243")
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            print("244")
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
            
            print(resume_lines)

            return resume_lines, text
        except KeyError:
            print('suma')
            
            text = textract.process(docx_file)
            text = text.decode("utf-8")
            clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
            return resume_lines, text
        try:
            clean_text = re.sub(r'\n+', '\n', text)
            clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if
                            line.strip()]  # Remove empty strings and whitespaces
            return resume_lines, text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "

    def convert_doc_to_txt(doc_file):
        try:
            print(doc_file)
            doc = aw.Document(doc_file)
            doc.save('True_Talent(doc_to_docx).docx')
            print("hello")
            text = docx2txt.process('True_Talent(doc_to_docx).docx')  # Extract text from docx file
            print("241")
            resume_lines = ""
            clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob            print("242")
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
            print('246')
            resume_lines = resume_lines[1:]
            resume_lines = resume_lines[:-3]
            print(resume_lines)
        
            return resume_lines, text
        except Exception as e:
            logging.error('Error in doc file:: ' + str(e))
            return [], " "




    def convert_pdf_to_txt(pdf_file):
        """
        A utility function to convert a machine-readable PDF to raw text.

        This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
        :param input_pdf_path: Path to the .pdf file which should be converted
        :type input_pdf_path: str
        :return: The text contents of the pdf
        :rtype: str
        """
        # try:
        #     #PDFMiner boilerplate
        #     pdf = pdfplumber.open(pdf_file)
        #     full_string= ""
        #     for page in pdf.pages:
        #       full_string += page.extract_text() + "\n"
        #     pdf.close()

            
        # try:

        #     raw_text = parser.from_file(pdf_file, service='text')['content']
        #     print("in try")
        # except RuntimeError as e:  
        try:
            print("in excpt")          
            # logging.error('Error in tika installation:: ' + str(e))
            # logging.error('--------------------------')
            # logging.error('Install java for better result ')
            pdf = pdfplumber.open(pdf_file)
            raw_text= ""
            for page in pdf.pages:
                raw_text += page.extract_text() + "\n"
                
            pdf.close()  
            print('out except 313')              
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
        try:
            full_string = re.sub(r'\n+', '\n', raw_text)
            full_string = full_string.replace("\r", "\n")
            full_string = full_string.replace("\t", " ")

            # Remove awkward LaTeX bullet characters

            full_string = re.sub(r"\uf0b7", " ", full_string)
            full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
            full_string = re.sub(r'• ', " ", full_string)

            # Split text blob into individual lines
            resume_lines = full_string.splitlines(True)

            # Remove empty strings and whitespaces
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
            print(resume_lines)
            return resume_lines, raw_text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
            
    def find_segment_indices(string_to_search, resume_segments, resume_indices):
        for i, line in enumerate(string_to_search):

            if line[0].islower():
                continue

            header = line.lower()

            if [o for o in resumeparse.objective if header.startswith(o)]:
                try:
                    resume_segments['objective'][header]
                except:
                    resume_indices.append(i)
                    header = [o for o in resumeparse.objective if header.startswith(o)][0]
                    resume_segments['objective'][header] = i
            elif [w for w in resumeparse.work_and_employment if header.startswith(w)]:
                try:
                    resume_segments['work_and_employment'][header]
                except:
                    resume_indices.append(i)
                    header = [w for w in resumeparse.work_and_employment if header.startswith(w)][0]
                    resume_segments['work_and_employment'][header] = i
            elif [e for e in resumeparse.education_and_training if header.startswith(e)]:
                try:
                    resume_segments['education_and_training'][header]
                except:
                    resume_indices.append(i)
                    header = [e for e in resumeparse.education_and_training if header.startswith(e)][0]
                    resume_segments['education_and_training'][header] = i
            elif [s for s in resumeparse.skills_header if header.startswith(s)]:
                try:
                    resume_segments['skills'][header]
                except:
                    resume_indices.append(i)
                    header = [s for s in resumeparse.skills_header if header.startswith(s)][0]
                    resume_segments['skills'][header] = i
            elif [m for m in resumeparse.misc if header.startswith(m)]:
                try:
                    resume_segments['misc'][header]
                except:
                    resume_indices.append(i)
                    header = [m for m in resumeparse.misc if header.startswith(m)][0]
                    resume_segments['misc'][header] = i
            elif [a for a in resumeparse.accomplishments if header.startswith(a)]:
                try:
                    resume_segments['accomplishments'][header]
                except:
                    resume_indices.append(i)
                    header = [a for a in resumeparse.accomplishments if header.startswith(a)][0]
                    resume_segments['accomplishments'][header] = i

    def slice_segments(string_to_search, resume_segments, resume_indices):
        resume_segments['contact_info'] = string_to_search[:resume_indices[0]]

        for section, value in resume_segments.items():
            if section == 'contact_info':
                continue

            for sub_section, start_idx in value.items():
                end_idx = len(string_to_search)
                if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                    end_idx = resume_indices[resume_indices.index(start_idx) + 1]

                resume_segments[section][sub_section] = string_to_search[start_idx:end_idx]

    def segment(string_to_search):
        resume_segments = {
            'objective': {},
            'work_and_employment': {},
            'education_and_training': {},
            'skills': {},
            'accomplishments': {},
            'misc': {}
        }

        resume_indices = []

        resumeparse.find_segment_indices(string_to_search, resume_segments, resume_indices)
        if len(resume_indices) != 0:
            resumeparse.slice_segments(string_to_search, resume_segments, resume_indices)
        else:
            resume_segments['contact_info'] = []

        return resume_segments

    
    def find_phone(text):
        try:
            return list(iter(phonenumbers.PhoneNumberMatcher(text, None)))[0].raw_string
        except:
            try:
                return re.search(
                    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                    text).group()
            except:
                return ""

    def extract_email(text):
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    
        
        
    
    def read_file(self, file, count_newfile, count_oldfile):
        """
        file : Give path of resume file
        docx_parser : Enter docx2txt or tika, by default is tika
        """
        # file = "/content/Asst Manager Trust Administration.docx"
        print("comming to file")
        print("\n\n\n\n File == ",file,"\n\n")
        
        count_newfile = int(count_newfile)
        count_oldfile = int(count_oldfile)
        print(count_newfile, "864")
        file = os.path.join(file)
        print("15")
        if file.endswith('docx'):
            print("in docx")
            resume_lines, raw_text = resumeparse.convert_docx_to_txt(file)
        
        elif file.endswith('doc') or file.endswith('.rtf'):
            print("in doc 781")
            resume_lines, raw_text = resumeparse.convert_doc_to_txt(file)
        
        elif file.endswith('pdf'):
            print("in pdf")
            resume_lines, raw_text = resumeparse.convert_pdf_to_txt(file)
        elif file.endswith('txt'):
            print("in txt")
            with open(file, 'r', encoding='latin') as f:
                resume_lines = f.readlines()

        else:
            resume_lines = None
        resume_segments = resumeparse.segment(resume_lines)
        print("2")
        
        full_text = " ".join(resume_lines)

        email = resumeparse.extract_email(full_text)
        print(email, "882")
        # phone = resumeparse.find_phone(full_text)
        
        
        def save_file(file_path, destination_directory, new_filename):
    
            if os.path.isfile(file_path):
        
                destination_path = os.path.join(destination_directory, new_filename)

        
                shutil.copy(file_path, destination_path)

                print(f"File saved successfully at: {destination_path}")
            else:
                print(f"Error: File not found at {file_path}")

        def save_file1(file_path, destination_directory, new_filename):
    
            if os.path.isfile(file_path):
        
                destination_path = os.path.join(destination_directory, new_filename)
                shutil.copy(file_path, destination_path)

                print(f"File saved successfully at: {destination_path}")
            else:
                print(f"Error: File not found at {file_path}")

        

        host = 'localhost'
        user = 'root'
        password = 'raje123456@'
        database = 'multi_threading'

        connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )

        cursor = connection.cursor()

        print(email)
        

        
        query = "SELECT Email FROM email WHERE Email = %s"
        cursor.execute(query, (email,))

        row = cursor.fetchone()

        if row:
            
            print(f"Row with ID {email} exists:")
            print(row)
            count_oldfile +=1
            file_path = file
            destination_directory = "./Old files"
            new_filename = file
            save_file(file_path, destination_directory, new_filename)
            
        else:
            
            print(f"Row with ID {email} does not exist.")
            count_newfile += 1
            file_path = file
            destination_directory = "./New File"
            new_filename = file
            save_file(file_path, destination_directory, new_filename)
            
        
        
         
        return {
            "email": email,
            #"phone": phone,
            "row_newfile": count_newfile,
            "row_oldfile": count_oldfile
            
        }
    
    def display(self):
        print("\n\n ========= Inside display() ========== \n\n")
        
        
parser_obj = resumeparse()
# parsed_resume_data = parser_obj.read_file('sample/Naukri_AbhijeetDey[8y_0m].doc')
# print("\n\n ========== parsed_data ========= \n\n")