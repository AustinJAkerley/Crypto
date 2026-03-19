import sys
import os

# Add parent directory to path to import crypto library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

# Import crypto library functions
from crypto.ciphers.number_field.rsa import rsa
from crypto.ciphers.number_field.dh import diffie_hellman
from crypto.common.random_prime import random_prime


# Authentication Views

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT tokens."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user."""
    return Response(UserSerializer(request.user).data)


# Crypto Views

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rsa_keygen(request):
    """
    Generate RSA key pair.
    
    Request body:
    {
        "num_bits": 512  // optional, default 512
    }
    """
    try:
        num_bits = request.data.get('num_bits', 512)
        
        # Validate num_bits
        if not isinstance(num_bits, int) or num_bits < 8:
            return Response(
                {'error': 'num_bits must be an integer >= 8'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate two random primes
        p = random_prime(num_bits)
        q = random_prime(num_bits)
        
        # Create RSA instance and generate e
        rsa_instance = rsa(p=p, q=q)
        e = rsa_instance.gen_e()
        N = rsa_instance.N
        
        return Response({
            'p': p,
            'q': q,
            'e': e,
            'N': N,
            'public_key': {'N': N, 'e': e},
            'private_key': {'p': p, 'q': q, 'e': e}
        })
    except Exception as exc:
        return Response(
            {'error': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rsa_encrypt(request):
    """
    Encrypt a message with RSA.
    
    Request body:
    {
        "m": 123,     // message (integer)
        "N": 456,     // modulus
        "e": 789      // public exponent
    }
    """
    try:
        m = request.data.get('m')
        N = request.data.get('N')
        e = request.data.get('e')
        
        if m is None or N is None or e is None:
            return Response(
                {'error': 'Missing required parameters: m, N, e'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert to integers
        try:
            m = int(m)
            N = int(N)
            e = int(e)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Parameters must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Encrypt
        rsa_instance = rsa(N=N, e=e)
        ciphertext = rsa_instance.encrypt(m)
        
        return Response({
            'ciphertext': ciphertext,
            'message': m,
            'N': N,
            'e': e
        })
    except Exception as exc:
        return Response(
            {'error': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rsa_decrypt(request):
    """
    Decrypt a ciphertext with RSA.
    
    Request body:
    {
        "c": 123,     // ciphertext (integer)
        "p": 456,     // prime p
        "q": 789,     // prime q
        "e": 101      // public exponent
    }
    """
    try:
        c = request.data.get('c')
        p = request.data.get('p')
        q = request.data.get('q')
        e = request.data.get('e')
        
        if c is None or p is None or q is None or e is None:
            return Response(
                {'error': 'Missing required parameters: c, p, q, e'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert to integers
        try:
            c = int(c)
            p = int(p)
            q = int(q)
            e = int(e)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Parameters must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Decrypt
        rsa_instance = rsa(p=p, q=q, e=e)
        plaintext = rsa_instance.decrypt(c)
        
        return Response({
            'plaintext': plaintext,
            'ciphertext': c,
            'p': p,
            'q': q,
            'e': e,
            'N': rsa_instance.N,
            'd': rsa_instance.d
        })
    except Exception as exc:
        return Response(
            {'error': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dh_exchange(request):
    """
    Perform Diffie-Hellman key exchange.
    
    Request body:
    {
        "g": 2,              // generator
        "p": 23,             // prime modulus
        "private_key": 6,    // your private key
        "B": 8               // other party's public key
    }
    """
    try:
        g = request.data.get('g')
        p = request.data.get('p')
        private_key = request.data.get('private_key')
        B = request.data.get('B')
        
        if g is None or p is None or private_key is None or B is None:
            return Response(
                {'error': 'Missing required parameters: g, p, private_key, B'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert to integers
        try:
            g = int(g)
            p = int(p)
            private_key = int(private_key)
            B = int(B)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Parameters must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Perform DH exchange
        dh = diffie_hellman(g=g, p=p, private_key=private_key, B=B)
        A = dh.A  # Your public key
        shared_key = dh.gen_shared_key()
        
        return Response({
            'shared_key': shared_key,
            'your_public_key': A,
            'their_public_key': B,
            'g': g,
            'p': p
        })
    except Exception as exc:
        return Response(
            {'error': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
