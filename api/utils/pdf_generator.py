"""
générateur de pdf professionnel avec reportlab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import Frame, PageTemplate, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os
import re

def header_footer(canvas, doc, title, author):
    """
    fonction appelée automatiquement pour chaque page
    dessine l'en-tête et le pied de page
    """
    canvas.saveState()
    
    page_width, page_height = A4
    
    # en-tête avec fond bleu
    canvas.setFillColor(colors.HexColor('#1e3a8a'))
    canvas.rect(0, page_height - 2*cm, page_width, 2*cm, fill=1, stroke=0)
    
    # texte blanc dans l'en-tête
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawString(2*cm, page_height - 1.3*cm, "SyntheSIA")
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(2*cm, page_height - 1.7*cm, "Rapport d'Intervention Technique")
    
    # logo png si disponible
    logo_path = os.path.join('assets', 'logo.png')
    if os.path.exists(logo_path):
        try:
            canvas.drawImage(
                logo_path,
                page_width - 3.5*cm,
                page_height - 1.8*cm,
                width=1.5*cm,
                height=1.5*cm,
                preserveAspectRatio=True,
                mask='auto'
            )
        except:
            pass
    
    # pied de page avec ligne et informations
    canvas.setStrokeColor(colors.HexColor('#e5e7eb'))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 2*cm, page_width - 2*cm, 2*cm)
    
    canvas.setFillColor(colors.HexColor('#6b7280'))
    canvas.setFont('Helvetica', 8)
    
    # date de génération à gauche
    canvas.drawString(
        2*cm, 
        1.5*cm, 
        f"Généré le {datetime.now().strftime('%d/%m/%Y a %H:%M')}"
    )
    
    # texte au centre
    canvas.drawCentredString(
        page_width / 2, 
        1.5*cm, 
        "Document confidentiel - Usage interne"
    )
    
    # numéro de page à droite
    canvas.drawRightString(
        page_width - 2*cm, 
        1.5*cm, 
        f"Page {canvas.getPageNumber()}"
    )
    
    canvas.restoreState()

def clean_markdown_formatting(text):
    """
    nettoie le texte des formats markdown et emojis
    convertit le markdown en html pour reportlab
    """
    # supprimer les titres markdown (# ## ###)
    text = re.sub(r'#{1,6}\s*', '', text)
    # convertir **gras** en <b>gras</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # convertir *italique* en <i>italique</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # supprimer les emojis (unicode)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", 
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # supprimer les séparateurs markdown (=== et ---)
    text = re.sub(r'={3,}', '', text)
    text = re.sub(r'-{3,}', '', text)
    
    # remplacer les puces spéciales par des tirets simples
    text = text.replace('■', '-')
    text = text.replace('●', '-')
    text = text.replace('•', '-')
    text = text.replace('◆', '-')
    text = text.replace('▸', '-')
    
    # normaliser les listes à puces
    text = re.sub(r'^\s*[-*+]\s+', '- ', text, flags=re.MULTILINE)
    
    return text

def detect_section_title(line):
    """
    détecte si une ligne est un titre de section
    cherche des mots-clés en majuscules
    """
    keywords = [
        'CONTEXTE', 'PROBLEME', 'DIAGNOSTIC', 'ACTIONS', 'RESULTATS', 
        'RECOMMANDATIONS', 'SUIVI', 'PHASE', 'ETAPE', 'CONFIGURATION',
        'TEST', 'VALIDATION', 'BILAN', 'INVENTAIRE', 'PREPARATION',
        'MAINTENANCE', 'LIVRABLE', 'SATISFACTION', 'METRICS', 'IMPACT'
    ]
    
    line_upper = line.upper().strip()
    
    # si la ligne est en majuscules et contient un mot-clé
    if line.isupper() and len(line) < 100:
        for keyword in keywords:
            if keyword in line_upper:
                return True
    
    return False

def create_pdf(title, content, author, role):
    """
    génère un pdf professionnel avec signature flexible
    
    param title: titre du rapport
    param content: contenu ia généré
    param author: nom de l'auteur
    param role: poste/rôle de l'auteur
    return: chemin complet du fichier pdf généré (dans /tmp pour vercel)
    """
    import tempfile
    
    # utiliser /tmp pour vercel (read-only sauf /tmp)
    # vercel est read-only sauf pour /tmp
    # on utilise tempfile pour créer un fichier temporaire
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # créer un fichier temporaire dans /tmp
    temp_file = tempfile.NamedTemporaryFile(
        mode='wb',
        suffix='.pdf',
        prefix=f'rapport_{timestamp}_',
        delete=False,
        dir='/tmp' if os.path.exists('/tmp') else None
    )
    filename = temp_file.name
    temp_file.close()
    
    print(f"création du pdf dans: {filename}")
    
    # créer le document pdf avec marges
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )
    
    # styles pour le document
    styles = getSampleStyleSheet()
    
    # style pour le titre principal
    style_title = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # style pour les titres de section (bien visibles)
    style_section = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leading=18,
        leftIndent=0,
        borderWidth=0,
        borderPadding=8
    )
    
    # style pour le contenu (bien différencié des titres)
    style_content = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=16,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#374151'),
        fontName='Helvetica'
    )
    
    # style pour les listes à puces
    style_bullet = ParagraphStyle(
        'BulletPoint',
        parent=style_content,
        fontSize=10,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6
    )
    
    # construction du contenu du pdf
    story = []
    
    # titre principal
    story.append(Paragraph(title, style_title))
    story.append(Spacer(1, 0.3*cm))
    
    # métadonnées dans un tableau
    metadata_data = [
        ['Date', datetime.now().strftime('%d/%m/%Y')],
        ['Heure', datetime.now().strftime('%H:%M')],
        ['Auteur', author],
        ['Poste', role],
        ['Type', 'Rapport d\'intervention technique'],
        ['Reference', f'SYNTH-{timestamp}']
    ]
    
    metadata_table = Table(metadata_data, colWidths=[4*cm, 12*cm])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 0.8*cm))
    
    # badge statut (vert)
    status_data = [['RAPPORT VALIDÉ - Document généré automatiquement par IA']]
    status_table = Table(status_data, colWidths=[16*cm])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d1fae5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#065f46')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(status_table)
    story.append(Spacer(1, 0.8*cm))
    
    # nettoyer le contenu et le formater
    content = clean_markdown_formatting(content)
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # détection des titres de section
        if detect_section_title(line):
            story.append(Spacer(1, 0.5*cm))
            
            # mettre le titre en gras
            story.append(Paragraph(f"<b>{line}</b>", style_section))
            
            # ligne décorative sous le titre
            line_data = [['  ']]
            line_table = Table(line_data, colWidths=[16*cm])
            line_table.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(line_table)
        
        # détection des listes à puces
        elif line.startswith('-') or line.startswith('•'):
            clean_line = re.sub(r'^[-•]\s*', '', line)
            story.append(Paragraph(f"- {clean_line}", style_bullet))
        
        # contenu normal
        else:
            story.append(Paragraph(line, style_content))
    
    # signature flexible (tableau)
    signature_data = [
        ['Rapport généré par', 'Valide par'],
        [author],
        [role],
    ]
    
    signature_table = Table(signature_data, colWidths=[8*cm, 8*cm])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(signature_table)
    
    # génération du pdf avec en-tête et pied de page
    def page_template(canvas, doc):
        header_footer(canvas, doc, title, author)
    
    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    
    print(f"pdf professionnel créé : {filename}")
    return filename
