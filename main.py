from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'config' / 'strategy.yaml'

def main():
    print('=' * 60)
    print('NIFTY BACKTESTER')
    print('=' * 60)
    print('Application started')
    with CONFIG.open(encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print('Timeframe:', config['timeframe'])
    print('Skeleton loaded successfully.')

if __name__ == '__main__':
    main()
