from typing import Dict, List

LANGUAGE_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    'JCL': {
        'patterns': [r'//\s*JOB\s+', r'//\s*EXEC\s+'],
        'keywords': ['JOB', 'EXEC', 'DD'],
        'extensions': ['.txt', '.jcl', '.JCL']
    },
    'COBOL': {
        'patterns': [r'IDENTIFICATION\s+DIVISION', r'PROCEDURE\s+DIVISION'],
        'keywords': ['DIVISION', 'SECTION', 'PERFORM'],
        'extensions': ['.txt', '.cbl', '.cob', '.CBL']
    },
    'ASM': {
        'patterns': [r'^\s*MACRO', r'^\s*CSECT'],
        'keywords': ['MACRO', 'CSECT', 'DS', 'DC'],
        'extensions': ['.txt', '.asm', '.ASM']
    },
    'PROC': {
        'patterns': [r'^\s*PROC\s+', r'^\s*PEND\s*$'],
        'keywords': ['PROC', 'PEND', 'SET'],
        'extensions': ['.txt', '.prc', '.PRC']
    },
    'COPY': {
        'patterns': [r'^\s*COPY\s+', r'^\s*INCLUDE\s+'],
        'keywords': ['COPY', 'INCLUDE'],
        'extensions': ['.txt', '.cpy', '.CPY']
    },
    'FORTRAN': {
        'patterns': [r'^\s*PROGRAM\s+', r'^\s*SUBROUTINE\s+'],
        'keywords': ['PROGRAM', 'SUBROUTINE', 'INTEGER'],
        'extensions': ['.txt', '.for', '.f', '.f77']
    },
    'NATURAL': {
        'patterns': [r'DEFINE\s+DATA', r'END-DEFINE'],
        'keywords': ['DEFINE DATA', 'END-DEFINE', 'WRITE'],
        'extensions': ['.txt', '.nsp', '.NSP']
    },
    'EASYTRIEVE': {
        'patterns': [r'^\s*PARM\s+', r'^\s*FILE\s+'],
        'keywords': ['PARM', 'FILE', 'SORT'],
        'extensions': ['.txt', '.ezt', '.EZT']
    },
    'SORT': {
        'patterns': [r'SORT\s+FIELDS', r'INCLUDE\s+COND'],
        'keywords': ['SORT FIELDS', 'INCLUDE COND', 'OUTREC'],
        'extensions': ['.txt', '.srt', '.SRT']
    },
    'Control-M': {
        'patterns': [r'IF\s+JOBRC', r'DOCOND'],
        'keywords': ['IF JOBRC', 'DOCOND', 'ENDDOCOND'],
        'extensions': ['.txt', '.ctm', '.CTM']
    },
    'ADS/O': {
        'patterns': [r'ACTIVITY', r'ENDACTIVITY'],
        'keywords': ['ACTIVITY', 'PROCESS', 'ENDACTIVITY'],
        'extensions': ['.txt', '.ads', '.ADS']
    },
    'CICS': {
        'patterns': [r'EXEC\s+CICS', r'DFHCOMMAREA'],
        'keywords': ['EXEC CICS', 'DFHCOMMAREA', 'SEND MAP'],
        'extensions': ['.txt', '.cic', '.CIC']
    },
    'DYL280': {
        'patterns': [r'DYL280', r'SEQUENCE'],
        'keywords': ['DYL280', 'REPORT', 'SEQUENCE'],
        'extensions': ['.txt', '.dyl', '.DYL']
    },
    'XDM_MAP': {
        'patterns': [r'DMAP', r'DFLD'],
        'keywords': ['DMAP', 'DSECT', 'DFLD'],
        'extensions': ['.txt', '.xmp', '.XMP']
    },
    'ADM_MAP': {
        'patterns': [r'MAP', r'FIELD'],
        'keywords': ['MAP', 'MEND', 'FIELD'],
        'extensions': ['.txt', '.amp', '.AMP']
    },
    'SYSIN': {
        'patterns': [r'/\*', r'SYSIN'],
        'keywords': ['/*', '//', 'SYSIN'],
        'extensions': ['.txt', '.sys', '.SYS']
    },
    'VSAM': {
        'patterns': [r'DEFINE\s+CLUSTER', r'INDEX'],
        'keywords': ['DEFINE', 'CLUSTER', 'INDEX'],
        'extensions': ['.txt', '.vsm', '.VSM']
    }
}

COMMENT_PATTERNS = {
    'general': [r'^\s*(/\*|\*/|//|#|\*|REM|--)', r'^\s*//', r'^\s*\*'],
    'COBOL': [r'^\s*\d{6}\s*\*'],
    'JCL': [r'^\s*//\*'],
    'ASM': [r'^\s*\*']
}
