import torch
import pickle
import io

# Step 1: Define a custom unpickler
class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        try:
            return super().find_class(module, name)
        except (AttributeError, ModuleNotFoundError):
            # Handle the unknown class/module by returning a dummy class/object
            print(f"Warning: Skipping unknown class {name} from module {module}")
            class UnknownClass:
                pass
            return UnknownClass

# Step 2: Define a custom module that uses the custom unpickler
class CustomPickleModule:
    Unpickler = SafeUnpickler

    @staticmethod
    def load(file, **kwargs):
        return SafeUnpickler(file, **kwargs).load()
    
    @staticmethod
    def loads(s, **kwargs):
        return SafeUnpickler(io.BytesIO(s), **kwargs).load()


# Step 3: Use the custom module with torch.load
# Assume 'model.pth' is the path to your PyTorch model file
model_path = 'model.pth'
loaded_data = torch.load(model_path, pickle_module=CustomPickleModule, map_location='cpu')

# Print the loaded data to verify the outcome
print(loaded_data)
