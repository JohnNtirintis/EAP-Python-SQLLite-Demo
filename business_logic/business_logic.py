
class BusinessLogic:
  """
  Business Logic Layer -εγκεφαλος εφαρμογης
  -κανει validation
  -εφαρμοζει κανονες
  -καλει το DAL για αποθηκευση
  """
  def__init__(self, dal):
     """
     κατασκευαζει την κλαση dal:
     το Data Acess Layer(επικοινωνια με βαση δεδομενων)
     """
  
    
     self.dal = dal
  def add_member(self, full_name, address, phone, mail, age, profession):
     """
     Προσθέτει νεο μελος στο συστημα
     Parametres:
     - full_name: ονοματεπωνυμο 
     - address: διευθυνση
     - phone: τηλεφωνο
     - email: email
     - age: ηλικια
     - profession: επάγγελμα

     Returns:
     - True , μηνυμα αν πετυχει
     - False, μηνυμα αν υπαρχει λαθος
     """
    # validation ονομα
    if not full_name:
        return False, " Πρέπει να συμπληρώσετε το ονοματεπώνυμο"
    # validation email
    if not email or "@" not in email:
        return False, "Μη έγκυρο email"
    # validation ηλικια  
    if age <= 0:
        return False, "Μη έγκυρη ηλικία"
    # δημιουργια dictionary με τα δεδομενα του μελους
    member_data = {
        "full_name": full_name,
        "adldress": address,
        "phone": phone,
        "email": email,
        "age": age,
        "profession": profession, 
        "active": True
    }
    # κληση DAL για αποθήκευση στη βάση
    self.dal.instert member(member data)
    # επιστροφη επιτυχιας
    return True, "Το μέλος προστέθηκε επιτυχώς
      
    
    
     
    


   
     
  
  




  
  
    
  
  
    
  
