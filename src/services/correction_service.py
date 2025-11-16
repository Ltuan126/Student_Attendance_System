from pathlib import Path
from typing import List, Optional
from models.correction import CorrectionRequest, CorrectionStatus



class CorrectionService:
    CORRECTIONS_FILE = Path("data/corrections.txt")
    
    def __init__(self, corrections_file: Optional[Path] = None):
        self.file_path = corrections_file or self.CORRECTIONS_FILE
        self._ensure_file_exists()
        self._request_counter = self._get_last_request_number()
    
    def _ensure_file_exists(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch()
    
    def _get_last_request_number(self) -> int:
        requests = self._read_all_requests()
        if not requests:
            return 0
        
        # Extract số từ request_id (CR0001 -> 1)
        numbers = []
        for req in requests:
            try:
                num = int(req.request_id.replace("CR", ""))
                numbers.append(num)
            except ValueError:
                continue
        
        return max(numbers) if numbers else 0
    
    def _generate_request_id(self) -> str:
        self._request_counter += 1
        return f"CR{self._request_counter:04d}"
    
    def _read_all_requests(self) -> List[CorrectionRequest]:
        requests = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        request = CorrectionRequest.from_line(line)
                        requests.append(request)
                    except ValueError as e:
                        print(f"[WARNING] Skip invalid line: {e}")
        return requests
    
    def _write_request(self, request: CorrectionRequest):
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(request.to_line() + '\n')
    
    def _update_request_in_file(self, request: CorrectionRequest):
        all_requests = self._read_all_requests()
        
        # Update request
        for i, req in enumerate(all_requests):
            if req.request_id == request.request_id:
                all_requests[i] = request
                break
        
        # Ghi lại toàn bộ file
        with open(self.file_path, 'w', encoding='utf-8') as f:
            for req in all_requests:
                f.write(req.to_line() + '\n')
    
    def request_correction(
        self, 
        student_id: str, 
        session_id: str,
        record_id: str, 
        reason: str,
        lecturer_id: str = "LEC001"
    ) -> bool:
        if not reason.strip():
            print("[ERROR] Reason cannot be empty")
            return False
        
        new_request = CorrectionRequest(
            request_id=self._generate_request_id(),
            student_id=student_id,
            session_id=session_id,
            record_id=record_id,
            reason=reason.strip(),
            status=CorrectionStatus.PENDING,
            lecturer_id=lecturer_id
        )
        
        self._write_request(new_request)
        print(f"[OK] Request recorded – Status: {new_request.status.value}")
        print(f"     Request ID: {new_request.request_id}")
        return True
    
    def list_pending_requests(self, lecturer_id: str) -> List[CorrectionRequest]:
        all_requests = self._read_all_requests()
        return [
            req for req in all_requests
            if req.lecturer_id == lecturer_id and req.status == CorrectionStatus.PENDING
        ]
    
    def approve_request(self, request_id: str, note: str = "") -> bool:
        all_requests = self._read_all_requests()
        
        # Tìm request
        request = None
        for req in all_requests:
            if req.request_id == request_id and req.status == CorrectionStatus.PENDING:
                request = req
                break
        
        if not request:
            print(f"[ERROR] Request {request_id} not found or not pending")
            return False
        
        # Update status
        request.status = CorrectionStatus.APPROVED
        request.note = note.strip() if note else None
        self._update_request_in_file(request)
        print(f"[MOCK] Updated attendance record {request.record_id} to PRESENT")
        
        print(f"[OK] Request #{request_id} approved")
        return True
    
    def reject_request(self, request_id: str, note: str = "") -> bool:
        all_requests = self._read_all_requests()
        
        # Tìm request
        request = None
        for req in all_requests:
            if req.request_id == request_id and req.status == CorrectionStatus.PENDING:
                request = req
                break
        
        if not request:
            print(f"[ERROR] Request {request_id} not found or not pending")
            return False
        
        # Update status
        request.status = CorrectionStatus.REJECTED
        request.note = note.strip() if note else None
        self._update_request_in_file(request)
        
        print(f"[OK] Request #{request_id} rejected")
        return True