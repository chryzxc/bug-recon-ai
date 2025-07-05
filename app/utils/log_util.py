from typing import Literal, overload
from colorama import Fore,Style
from enum import Enum

class LogType(Enum):
    
    INITIALIZE="initialize",
    INVALID_TARGET ='invalid_target',
    SCANNING='scanning',
    ANALYZING='analyzing',
    CRAWLING='crawling',
    ERROR='error',
    OUTPUT_FILE_NOT_FOUND='output_file_not_found',
    COMPLETED='completed',
    PARSING='parsing',
    PARSE_ERROR='parse_error'
    GENERATING_REPORTS="generating_reports",
    REPORTS_SAVED='reports_saved'
    
@overload
def logger(log_type: Literal[LogType.ERROR], *,error: str) -> str: ...
@overload
def logger(log_type: Literal[LogType.PARSE_ERROR],*, error: str) -> str: ...
@overload
def logger(log_type: Literal[LogType.ANALYZING], *,target: str) -> str: ...
@overload
def logger(log_type: Literal[LogType.SCANNING], *,target: str) -> str: ...
@overload
def logger(log_type: Literal[LogType.CRAWLING], *,target: str) -> str: ...
def logger(log_type: LogType,module_name:str="Bug Recon AI",target:str="",error:str=""):
    match log_type:
        case LogType.INITIALIZE:
            return print(Fore.YELLOW + f"[{module_name}] Initializing....." + Style.RESET_ALL)
        case LogType.INVALID_TARGET:
            return print(Fore.RED + f"[{module_name}] Closing because target is not a valid subdomain" + Style.RESET_ALL)
        case LogType.SCANNING:
            return print(Fore.YELLOW + f"[{module_name}] Scanning target: {target}" + Style.RESET_ALL)
        case LogType.ANALYZING:
            return print(Fore.YELLOW + f"[{module_name}] Analyzing target: {target}" + Style.RESET_ALL)
        case LogType.CRAWLING:
            return print(Fore.YELLOW + f"[{module_name}] Crawling target: {target}" + Style.RESET_ALL)
        case LogType.ERROR:
            return print(Fore.RED + f"[{module_name}] Error: {error}" + Style.RESET_ALL)
        case LogType.OUTPUT_FILE_NOT_FOUND:
            return print(Fore.RED + f"[{module_name}] No outfile file found... Exiting" + Style.RESET_ALL)
        case LogType.COMPLETED:
            return print(Fore.YELLOW + f"[{module_name}] Inspect completed" + Style.RESET_ALL)
        case LogType.PARSING:
            return print(Fore.YELLOW + f"[{module_name}] Parsing results..." + Style.RESET_ALL)
        case LogType.PARSE_ERROR:
            return print(Fore.RED + f"[{module_name}] Error parsing results: {error}" + Style.RESET_ALL)
        case LogType.GENERATING_REPORTS:
            return print(Fore.CYAN + f"[{module_name}] Generating reports.... Please wait" + Style.RESET_ALL)
        case LogType.REPORTS_SAVED:
            return print(Fore.CYAN + f"[{module_name}] Reports saved to: /{target}" + Style.RESET_ALL)
