"""
Script pour tester la santé de tous les services
"""
import requests
import sys
from typing import Dict, Any

SERVICES = {
    "API Gateway": "http://localhost:8000/health",
    "Parser Service": "http://localhost:8001/health",
    "NLP Service": "http://localhost:8003/health",
    "LCA Service": "http://localhost:8004/health",
    "Scoring Service": "http://localhost:8005/health"
}


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def test_service(name: str, url: str) -> Dict[str, Any]:
    """Teste un service"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "healthy",
                "data": data,
                "error": None
            }
        else:
            return {
                "status": "unhealthy",
                "data": None,
                "error": f"HTTP {response.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            "status": "unreachable",
            "data": None,
            "error": "Service non accessible"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": str(e)
        }


def main():
    print(f"\n{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'VERIFICATION DE LA SANTE DES SERVICES'.center(80)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")
    
    results = {}
    all_healthy = True
    
    for name, url in SERVICES.items():
        print(f"{Colors.BLUE}Test de {name}...{Colors.RESET}", end=" ")
        result = test_service(name, url)
        results[name] = result
        
        if result["status"] == "healthy":
            print(f"{Colors.GREEN}[OK]{Colors.RESET}")
            if result["data"]:
                db_status = result["data"].get("database_connected", None)
                if db_status is not None:
                    db_icon = "[OK]" if db_status else "[KO]"
                    print(f"  {db_icon} Database: {'Connectee' if db_status else 'Non connectee'}")
        elif result["status"] == "unreachable":
            print(f"{Colors.RED}[INACCESSIBLE]{Colors.RESET}")
            all_healthy = False
        else:
            print(f"{Colors.YELLOW}[{result['status'].upper()}]{Colors.RESET}")
            if result["error"]:
                print(f"  Erreur: {result['error']}")
            all_healthy = False
    
    print(f"\n{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    if all_healthy:
        print(f"{Colors.GREEN}{Colors.BOLD}[SUCCESS] Tous les services sont operationnels{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}[WARNING] Certains services ont des problemes{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Pour demarrer les services:{Colors.RESET}")
        print(f"  {Colors.CYAN}docker-compose up -d{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")
    
    return all_healthy


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
