#!/usr/bin/env python3
"""
Fantasy Name Generator
Generates names for humans, elves, dwarves, and orcs using syllable combination.

Usage as standalone:
    python namegen.py human -n 10
    python namegen.py elf --seed 12345

Usage as library:
    from namegen import NameGenerator
    gen = NameGenerator()
    name = gen.generate_human_name()
"""

import json
import random
import argparse
from pathlib import Path


class NameGenerator:
    """Generates fantasy names based on race and loaded syllable data."""
    
    def __init__(self, data_file='name_data.json'):
        """
        Load name data from JSON file.
        
        Args:
            data_file: Path to JSON file with syllable data
        """
        # Handle both relative and absolute paths
        if not Path(data_file).is_absolute():
            data_path = Path(__file__).parent / data_file
        else:
            data_path = Path(data_file)
            
        with open(data_path, 'r') as f:
            self.data = json.load(f)
    
    def generate_human_name(self, seed=None):
        """
        Generate a human name.
        
        Args:
            seed: Optional random seed for reproducible results
            
        Returns:
            String in format "FirstName Surname"
        """
        if seed is not None:
            random.seed(seed)
        
        first = (random.choice(self.data['human']['first_start']) + 
                random.choice(self.data['human']['first_end']))
        
        last = (random.choice(self.data['human']['surname_prefix']) + 
               random.choice(self.data['human']['surname_suffix']))
        
        return f"{first.capitalize()} {last.capitalize()}"
    
    def generate_elf_name(self, seed=None):
        """
        Generate an elf name.
        
        Args:
            seed: Optional random seed for reproducible results
            
        Returns:
            String in format "FirstName Surname"
        """
        if seed is not None:
            random.seed(seed)
        
        first = (random.choice(self.data['elf']['first_start']) + 
                random.choice(self.data['elf']['first_end']))
        
        last = (random.choice(self.data['elf']['surname_prefix']) + 
               random.choice(self.data['elf']['surname_suffix']))
        
        return f"{first.capitalize()} {last.capitalize()}"
    
    def generate_dwarf_name(self, seed=None):
        """
        Generate a dwarf name.
        
        Args:
            seed: Optional random seed for reproducible results
            
        Returns:
            String in format "FirstName Surname"
        """
        if seed is not None:
            random.seed(seed)
        
        first = (random.choice(self.data['dwarf']['first_start']) + 
                random.choice(self.data['dwarf']['first_end']))
        
        last = (random.choice(self.data['dwarf']['surname_prefix']) + 
               random.choice(self.data['dwarf']['surname_suffix']))
        
        return f"{first.capitalize()} {last.capitalize()}"
    
    def generate_orc_name(self, seed=None):
        """
        Generate an orc name (50% chance of title).
        
        Args:
            seed: Optional random seed for reproducible results
            
        Returns:
            String, either "Name" or "Name Title"
        """
        if seed is not None:
            random.seed(seed)
        
        name = (random.choice(self.data['orc']['first_start']) + 
               random.choice(self.data['orc']['first_end']))
        
        # 50% chance to add a title
        if random.random() > 0.5:
            title = random.choice(self.data['orc']['titles'])
            return f"{name.capitalize()} {title}"
        
        return name.capitalize()
    
    def generate_name(self, race, seed=None):
        """
        Generate a name for the specified race.
        
        Args:
            race: One of 'human', 'elf', 'dwarf', 'orc'
            seed: Optional random seed for reproducible results
            
        Returns:
            Generated name string
            
        Raises:
            ValueError: If race is not recognized
        """
        race = race.lower()
        
        if race == 'human':
            return self.generate_human_name(seed)
        elif race == 'elf':
            return self.generate_elf_name(seed)
        elif race == 'dwarf':
            return self.generate_dwarf_name(seed)
        elif race == 'orc':
            return self.generate_orc_name(seed)
        else:
            raise ValueError(
                f"Unknown race: {race}. Choose from: human, elf, dwarf, orc"
            )
    
    def generate_batch(self, race, count=10, seed=None):
        """
        Generate multiple names for a race.
        
        Args:
            race: One of 'human', 'elf', 'dwarf', 'orc'
            count: Number of names to generate
            seed: Optional base random seed
            
        Returns:
            List of generated name strings
        """
        if seed is not None:
            random.seed(seed)
        
        names = []
        for i in range(count):
            # Use different seed for each name if base seed provided
            name_seed = seed + i if seed is not None else None
            names.append(self.generate_name(race, name_seed))
        
        return names


# CLI functionality - only runs when script is executed directly
def main():
    """Command-line interface for the name generator."""
    parser = argparse.ArgumentParser(
        description='Generate fantasy names for RPG characters and NPCs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s human                    # Generate 10 human names
  %(prog)s elf -n 20                # Generate 20 elf names
  %(prog)s dwarf --seed 12345       # Reproducible dwarf names
  %(prog)s orc -n 5 -s 999          # 5 orc names with seed
        """
    )
    
    parser.add_argument(
        'race',
        choices=['human', 'elf', 'dwarf', 'orc'],
        help='Race to generate names for'
    )
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=10,
        help='Number of names to generate (default: 10)'
    )
    parser.add_argument(
        '-s', '--seed',
        type=int,
        help='Random seed for reproducible results'
    )
    parser.add_argument(
        '--data-file',
        default='name_data.json',
        help='Path to JSON data file (default: name_data.json)'
    )
    
    args = parser.parse_args()
    
    try:
        # Generate names
        generator = NameGenerator(args.data_file)
        names = generator.generate_batch(args.race, args.count, args.seed)
        
        # Print results
        print(f"\n{args.race.capitalize()} Names:")
        print("=" * 50)
        for i, name in enumerate(names, 1):
            print(f"{i:3}. {name}")
        print()
        
    except FileNotFoundError:
        print(f"Error: Could not find data file '{args.data_file}'")
        print("Make sure name_data.json is in the same directory as this script.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


# This block only runs when the script is executed directly
# It does NOT run when the module is imported
if __name__ == '__main__':
    exit(main())