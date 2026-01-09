"""Export components for Resume Analyzer Core"""
import streamlit as st
import json
import csv
from io import StringIO, BytesIO
from typing import Dict, List, Any, Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from src.models.profile_analysis import ProfileAnalysis
from src.models.profile_url import ProfileURL


def render_export_options(
    profile_analyses: Dict[str, ProfileAnalysis],
    profile_urls: Optional[Dict[str, ProfileURL]] = None,
    resume_analysis: Optional[Dict] = None
):
    """
    Render export options for analysis results.

    Args:
        profile_analyses: Dictionary of profile analyses keyed by platform
        profile_urls: Optional dictionary of profile URLs
        resume_analysis: Optional resume analysis results
    """
    st.subheader("📤 Export Analysis Results")

    if not profile_analyses:
        st.warning("No analysis results available to export.")
        return

    # Create columns for different export options
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 PDF Report", key="export_pdf", help="Export as professional PDF report"):
            pdf_buffer = generate_pdf_report(profile_analyses, profile_urls, resume_analysis)
            st.download_button(
                label="Download PDF Report",
                data=pdf_buffer,
                file_name=f"profile_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

    with col2:
        if st.button("📑 JSON Data", key="export_json", help="Export as JSON data file"):
            json_str = generate_json_export(profile_analyses, profile_urls, resume_analysis)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"profile_analysis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    with col3:
        if st.button("📊 CSV Summary", key="export_csv", help="Export as CSV summary"):
            csv_str = generate_csv_summary(profile_analyses, profile_urls)
            st.download_button(
                label="Download CSV",
                data=csv_str,
                file_name=f"profile_analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col4:
        if st.button("📋 Text Report", key="export_txt", help="Export as plain text report"):
            txt_str = generate_text_report(profile_analyses, profile_urls, resume_analysis)
            st.download_button(
                label="Download TXT",
                data=txt_str,
                file_name=f"profile_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


def generate_pdf_report(
    profile_analyses: Dict[str, ProfileAnalysis],
    profile_urls: Optional[Dict[str, ProfileURL]] = None,
    resume_analysis: Optional[Dict] = None
) -> BytesIO:
    """
    Generate a professional PDF report of the analysis results.

    Args:
        profile_analyses: Dictionary of profile analyses keyed by platform
        profile_urls: Optional dictionary of profile URLs
        resume_analysis: Optional resume analysis results

    Returns:
        BytesIO buffer containing the PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    story.append(Paragraph("Profile Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Date
    date_para = Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", styles['Normal'])
    story.append(date_para)
    story.append(Spacer(1, 20))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Spacer(1, 12))

    # Summary table
    summary_data = [['Profile Type', 'Overall Score', 'Clarity Score', 'Impact Score']]
    for platform, analysis in profile_analyses.items():
        summary_data.append([
            platform.title(),
            f"{analysis.overall_score:.1f}/100",
            f"{analysis.clarity_score:.1f}/100",
            f"{analysis.impact_score:.1f}/100"
        ])

    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # Individual Profile Analyses
    for platform, analysis in profile_analyses.items():
        story.append(Paragraph(f"{platform.title()} Profile Analysis", styles['Heading2']))
        story.append(Spacer(1, 12))

        # Scores
        scores_text = f"""
        <b>Overall Score:</b> {analysis.overall_score:.1f}/100<br/>
        <b>Clarity Score:</b> {analysis.clarity_score:.1f}/100<br/>
        <b>Impact Score:</b> {analysis.impact_score:.1f}/100
        """
        story.append(Paragraph(scores_text, styles['Normal']))
        story.append(Spacer(1, 12))

        # Strengths
        if analysis.strengths:
            story.append(Paragraph("Strengths:", styles['Heading3']))
            for strength in analysis.strengths:
                story.append(Paragraph(f"• {strength}", styles['Normal']))
            story.append(Spacer(1, 6))

        # Weaknesses
        if analysis.weaknesses:
            story.append(Paragraph("Areas for Improvement:", styles['Heading3']))
            for weakness in analysis.weaknesses:
                story.append(Paragraph(f"• {weakness}", styles['Normal']))
            story.append(Spacer(1, 6))

        # Suggestions
        if analysis.suggestions:
            story.append(Paragraph("Improvement Suggestions:", styles['Heading3']))
            for suggestion in analysis.suggestions:
                if isinstance(suggestion, dict):
                    title = suggestion.get('title', 'N/A')
                    desc = suggestion.get('description', 'No description')
                else:
                    # Assuming suggestion is an object with attributes
                    title = getattr(suggestion, 'title', 'N/A')
                    desc = getattr(suggestion, 'description', 'No description')

                story.append(Paragraph(f"• <b>{title}:</b> {desc}", styles['Normal']))
            story.append(Spacer(1, 12))

        # Detailed feedback
        if analysis.detailed_feedback:
            story.append(Paragraph("Detailed Feedback:", styles['Heading3']))
            story.append(Paragraph(analysis.detailed_feedback, styles['Normal']))

        story.append(PageBreak())

    # Build the PDF
    doc.build(story)

    # Move buffer pointer to the beginning
    buffer.seek(0)
    return buffer


def generate_json_export(
    profile_analyses: Dict[str, ProfileAnalysis],
    profile_urls: Optional[Dict[str, ProfileURL]] = None,
    resume_analysis: Optional[Dict] = None
) -> str:
    """
    Generate JSON export of the analysis results.

    Args:
        profile_analyses: Dictionary of profile analyses keyed by platform
        profile_urls: Optional dictionary of profile URLs
        resume_analysis: Optional resume analysis results

    Returns:
        JSON string with the analysis data
    """
    export_data = {
        "export_date": datetime.now().isoformat(),
        "analyses": {},
        "urls": {},
        "resume_analysis": resume_analysis
    }

    # Add profile analyses
    for platform, analysis in profile_analyses.items():
        export_data["analyses"][platform] = {
            "profile_type": analysis.profile_type,
            "overall_score": analysis.overall_score,
            "clarity_score": analysis.clarity_score,
            "impact_score": analysis.impact_score,
            "strengths": analysis.strengths,
            "weaknesses": analysis.weaknesses,
            "suggestions": [],
            "detailed_feedback": analysis.detailed_feedback,
            "extraction_timestamp": analysis.extraction_timestamp.isoformat() if analysis.extraction_timestamp else None
        }

        # Handle suggestions (could be dict or object)
        for suggestion in analysis.suggestions:
            if isinstance(suggestion, dict):
                export_data["analyses"][platform]["suggestions"].append(suggestion)
            else:
                # Convert object to dict
                suggestion_dict = {
                    "title": getattr(suggestion, 'title', ''),
                    "description": getattr(suggestion, 'description', ''),
                    "category": getattr(suggestion, 'category', ''),
                    "priority": getattr(suggestion, 'priority', '')
                }
                export_data["analyses"][platform]["suggestions"].append(suggestion_dict)

    # Add profile URLs if available
    if profile_urls:
        for platform, url_obj in profile_urls.items():
            if url_obj:
                export_data["urls"][platform] = {
                    "url": url_obj.url,
                    "profile_type": url_obj.profile_type,
                    "is_valid": url_obj.is_valid,
                    "is_accessible": url_obj.is_accessible,
                    "validation_timestamp": url_obj.validation_timestamp.isoformat() if url_obj.validation_timestamp else None
                }

    return json.dumps(export_data, indent=2)


def generate_csv_summary(
    profile_analyses: Dict[str, ProfileAnalysis],
    profile_urls: Optional[Dict[str, ProfileURL]] = None
) -> str:
    """
    Generate CSV summary of the analysis results.

    Args:
        profile_analyses: Dictionary of profile analyses keyed by platform
        profile_urls: Optional dictionary of profile URLs

    Returns:
        CSV string with the summary data
    """
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    header = ["Profile Type", "URL", "Overall Score", "Clarity Score", "Impact Score",
              "Strengths Count", "Weaknesses Count", "Suggestions Count"]
    writer.writerow(header)

    # Write data rows
    for platform, analysis in profile_analyses.items():
        url = "N/A"
        if profile_urls and platform in profile_urls and profile_urls[platform]:
            url = profile_urls[platform].url

        row = [
            platform.title(),
            url,
            f"{analysis.overall_score:.2f}",
            f"{analysis.clarity_score:.2f}",
            f"{analysis.impact_score:.2f}",
            len(analysis.strengths),
            len(analysis.weaknesses),
            len(analysis.suggestions)
        ]
        writer.writerow(row)

    return output.getvalue()


def generate_text_report(
    profile_analyses: Dict[str, ProfileAnalysis],
    profile_urls: Optional[Dict[str, ProfileURL]] = None,
    resume_analysis: Optional[Dict] = None
) -> str:
    """
    Generate text report of the analysis results.

    Args:
        profile_analyses: Dictionary of profile analyses keyed by platform
        profile_urls: Optional dictionary of profile URLs
        resume_analysis: Optional resume analysis results

    Returns:
        Text string with the report
    """
    report_lines = [
        "Profile Analysis Report",
        "=" * 50,
        f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}",
        ""
    ]

    # Add executive summary
    report_lines.extend([
        "EXECUTIVE SUMMARY",
        "-" * 20
    ])

    for platform, analysis in profile_analyses.items():
        url = "N/A"
        if profile_urls and platform in profile_urls and profile_urls[platform]:
            url = profile_urls[platform].url

        report_lines.extend([
            f"",
            f"{platform.upper()} PROFILE:",
            f"  URL: {url}",
            f"  Overall Score: {analysis.overall_score:.1f}/100",
            f"  Clarity Score: {analysis.clarity_score:.1f}/100",
            f"  Impact Score: {analysis.impact_score:.1f}/100",
            f"  Strengths: {len(analysis.strengths)} identified",
            f"  Weaknesses: {len(analysis.weaknesses)} identified",
            f"  Suggestions: {len(analysis.suggestions)} provided"
        ])

    # Add detailed analysis for each profile
    for platform, analysis in profile_analyses.items():
        report_lines.extend([
            "",
            f"DETAILED {platform.upper().replace(' ', '_')} ANALYSIS",
            "-" * 30,
            f"Overall Score: {analysis.overall_score}/100",
            f"Clarity Score: {analysis.clarity_score}/100",
            f"Impact Score: {analysis.impact_score}/100",
            ""
        ])

        if analysis.strengths:
            report_lines.append("STRENGTHS:")
            for strength in analysis.strengths:
                report_lines.append(f"  • {strength}")
            report_lines.append("")

        if analysis.weaknesses:
            report_lines.append("AREAS FOR IMPROVEMENT:")
            for weakness in analysis.weaknesses:
                report_lines.append(f"  • {weakness}")
            report_lines.append("")

        if analysis.suggestions:
            report_lines.append("IMPROVEMENT SUGGESTIONS:")
            for suggestion in analysis.suggestions:
                if isinstance(suggestion, dict):
                    title = suggestion.get('title', 'N/A')
                    desc = suggestion.get('description', 'No description')
                else:
                    title = getattr(suggestion, 'title', 'N/A')
                    desc = getattr(suggestion, 'description', 'No description')

                report_lines.append(f"  • {title}: {desc}")
            report_lines.append("")

        if analysis.detailed_feedback:
            report_lines.extend([
                "DETAILED FEEDBACK:",
                f"  {analysis.detailed_feedback}",
                ""
            ])

    # Add resume analysis if available
    if resume_analysis:
        report_lines.extend([
            "RESUME ANALYSIS COMPARISON",
            "-" * 30
        ])
        # Add resume analysis details here if needed

    return "\n".join(report_lines)


def render_share_options():
    """Render options for sharing the analysis results."""
    st.subheader("🔗 Share Results")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "Share your analysis results with others by exporting to your preferred format.\n\n"
            "PDF reports are ideal for sharing with mentors or colleagues.\n\n"
            "JSON exports are useful for further processing or integration with other tools."
        )

    with col2:
        st.success(
            "**Privacy Notice:**\n"
            "All analysis happens locally in your browser.\n"
            "No profile data is stored on our servers.\n"
            "Exported files only contain information you've provided."
        )


def get_export_formats() -> List[Dict[str, str]]:
    """
    Get available export formats with descriptions.

    Returns:
        List of dictionaries with format information
    """
    return [
        {
            "format": "PDF",
            "description": "Professional report with formatted analysis results",
            "use_case": "Sharing with mentors, colleagues, or for personal records"
        },
        {
            "format": "JSON",
            "description": "Structured data export for further processing",
            "use_case": "Integration with other tools or custom analysis"
        },
        {
            "format": "CSV",
            "description": "Tabular summary of key metrics",
            "use_case": "Spreadsheet analysis or comparison across multiple profiles"
        },
        {
            "format": "TXT",
            "description": "Plain text report for simple review",
            "use_case": "Quick review or basic documentation"
        }
    ]


def validate_export_data(
    profile_analyses: Dict[str, ProfileAnalysis],
    profile_urls: Optional[Dict[str, ProfileURL]] = None
) -> tuple[bool, List[str]]:
    """
    Validate export data to ensure completeness.

    Args:
        profile_analyses: Dictionary of profile analyses
        profile_urls: Optional dictionary of profile URLs

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    if not profile_analyses:
        issues.append("No profile analyses available for export")

    for platform, analysis in profile_analyses.items():
        if analysis.overall_score < 0 or analysis.overall_score > 100:
            issues.append(f"Invalid overall score for {platform}: {analysis.overall_score}")

        if analysis.clarity_score < 0 or analysis.clarity_score > 100:
            issues.append(f"Invalid clarity score for {platform}: {analysis.clarity_score}")

        if analysis.impact_score < 0 or analysis.impact_score > 100:
            issues.append(f"Invalid impact score for {platform}: {analysis.impact_score}")

    return len(issues) == 0, issues