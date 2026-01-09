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
    Fonction appelée automatiquement pour CHAQUE page
    Dessine l'en-tête et le pied de page
    """
    canvas.saveState()
    
    page_width, page_height = A4
    
    # EN-TÊTE
    canvas.setFillColor(colors.HexColor('#1e3a8a'))
    canvas.rect(0, page_height - 2*cm, page_width, 2*cm, fill=1, stroke=0)
    
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawString(2*cm, page_height - 1.3*cm, "SyntheSIA")
    
    canvas.setFont('Helvetica', 10)
    canvas.drawString(2*cm, page_height - 1.7*cm, "Rapport d'Intervention Technique")
    
    # Logo PNG
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
    
    # PIED DE PAGE
    canvas.setStrokeColor(colors.HexColor('#e5e7eb'))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 2*cm, page_width - 2*cm, 2*cm)
    
    canvas.setFillColor(colors.HexColor('#6b7280'))
    canvas.setFont('Helvetica', 8)
    
    canvas.drawString(
        2*cm, 
        1.5*cm, 
        f"Généré le {datetime.now().strftime('%d/%m/%Y a %H:%M')}"
    )
    
    canvas.drawCentredString(
        page_width / 2, 
        1.5*cm, 
        "Document confidentiel - Usage interne"
    )
    
    canvas.drawRightString(
        page_width - 2*cm, 
        1.5*cm, 
        f"Page {canvas.getPageNumber()}"
    )
    
    canvas.restoreState()

def clean_markdown_formatting(text):
    """Nettoie le texte des formats Markdown et emojis"""
    
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # Supprimer emojis
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
    
    # Supprimer les séparateurs disgracieux
    text = re.sub(r'={3,}', '', text)  # ← SUPPRIME ===
    text = re.sub(r'-{3,}', '', text)  # ← SUPPRIME ---
    
    text = text.replace('■', '-')
    text = text.replace('●', '-')
    text = text.replace('•', '-')
    text = text.replace('◆', '-')
    text = text.replace('▸', '-')
    
    text = re.sub(r'^\s*[-*+]\s+', '- ', text, flags=re.MULTILINE)
    
    return text

def detect_section_title(line):
    """Détecte si une ligne est un titre de section"""
    keywords = [
        'CONTEXTE', 'PROBLEME', 'DIAGNOSTIC', 'ACTIONS', 'RESULTATS', 
        'RECOMMANDATIONS', 'SUIVI', 'PHASE', 'ETAPE', 'CONFIGURATION',
        'TEST', 'VALIDATION', 'BILAN', 'INVENTAIRE', 'PREPARATION',
        'MAINTENANCE', 'LIVRABLE', 'SATISFACTION', 'METRICS', 'IMPACT'
    ]
    
    line_upper = line.upper().strip()
    
    if line.isupper() and len(line) < 100:
        for keyword in keywords:
            if keyword in line_upper:
                return True
    
    return False

def create_pdf(title, content, author, role):
    """
    Génère un PDF professionnel avec signature flexible
    
    Args:
        title: Titre du rapport
        content: Contenu IA
        author: Nom de l'auteur
        role: Poste/rôle de l'auteur
    
    Returns:
        str: Chemin complet du fichier PDF généré (dans /tmp pour Vercel)
    """
    import tempfile
    
    # ═══════════════════════════════════════════════════════
    # UTILISER /tmp POUR VERCEL (read-only sauf /tmp)
    # ═══════════════════════════════════════════════════════
    # Vercel est read-only sauf pour /tmp
    # On utilise tempfile pour créer un fichier temporaire
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Créer un fichier temporaire dans /tmp
    temp_file = tempfile.NamedTemporaryFile(
        mode='wb',
        suffix='.pdf',
        prefix=f'rapport_{timestamp}_',
        delete=False,
        dir='/tmp' if os.path.exists('/tmp') else None
    )
    filename = temp_file.name
    temp_file.close()
    
    print(f"📄 Création du PDF dans: {filename}")
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )
    
    # STYLES
    styles = getSampleStyleSheet()
    
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
    
    # Style pour les titres de section (bien visibles)
    style_section = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,                              # ← AUGMENTÉ (était 13)
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=20,                           # ← PLUS D'ESPACE AVANT
        fontName='Helvetica-Bold',
        leading=18,
        leftIndent=0,
        # Ajout d'un trait sous le titre pour bien le distinguer
        borderWidth=0,
        borderPadding=8
    )
    
    # Style pour le contenu (bien différencié des titres)
    style_content = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,                              # ← Contenu plus petit que titres
        leading=16,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#374151'),
        fontName='Helvetica'                      # ← Normal (pas Bold)
    )
    
    style_bullet = ParagraphStyle(
        'BulletPoint',
        parent=style_content,
        fontSize=10,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6
    )
    
    # CONSTRUCTION
    story = []
    
    # Titre
    story.append(Paragraph(title, style_title))
    story.append(Spacer(1, 0.3*cm))
    
    # Métadonnées
    metadata_data = [
        ['Date', datetime.now().strftime('%d/%m/%Y')],
        ['Heure', datetime.now().strftime('%H:%M')],
        ['Auteur', author],
        ['Poste', role],  # ← NOUVEAU
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
    
    # Badge statut
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
    
    # Nettoyer le contenu
    content = clean_markdown_formatting(content)
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # DÉTECTION AMÉLIORÉE DES TITRES DE SECTION
        if detect_section_title(line):
            story.append(Spacer(1, 0.5*cm))  # Espace avant le titre
            
            # Mettre le titre en majuscules ET gras avec trait de séparation visuel
            story.append(Paragraph(f"<b>{line}</b>", style_section))
            
            # Ligne décorative sous le titre
            line_data = [['  ']]
            line_table = Table(line_data, colWidths=[16*cm])
            line_table.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(line_table)
        
        # Détection des listes à puces
        elif line.startswith('-') or line.startswith('•'):
            clean_line = re.sub(r'^[-•]\s*', '', line)
            story.append(Paragraph(f"- {clean_line}", style_bullet))
        
        # Contenu normal
        else:
            story.append(Paragraph(line, style_content))
    
    # SIGNATURE FLEXIBLE
    signature_data = [
        ['Rapport généré par', 'Valide par'],
        [author],
        [role],  # ← LIGNES VIDES
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
    
    # GÉNÉRATION
    def page_template(canvas, doc):
        header_footer(canvas, doc, title, author)
    
    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    
    print(f"✅ PDF professionnel créé : {filename}")
    return filename